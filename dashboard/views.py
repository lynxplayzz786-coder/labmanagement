import json
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from accounts.decorators import login_required_custom


@login_required_custom
def index(request):
    role = request.user.role
    if role == 'admin':
        return render(request, 'dashboard/admin_dashboard.html', _admin_context(request))
    elif role == 'staff':
        return render(request, 'dashboard/staff_dashboard.html', _staff_context(request))
    else:
        return render(request, 'dashboard/student_dashboard.html', _student_context(request))


@login_required_custom
def reports(request):
    if request.user.role != 'admin':
        from django.contrib import messages
        messages.error(request, "Access denied.")
        return redirect('dashboard:index')
    return render(request, 'dashboard/reports.html', _reports_context(request))


# ─── Admin Context ────────────────────────────────────────────────────────────

def _admin_context(request):
    from equipment.models import Equipment, Category
    from bookings.models import Booking, Maintenance

    # Stat cards
    total_equipment     = Equipment.objects.count()
    available_equipment = Equipment.objects.filter(status='available').count()
    issued_count        = Booking.objects.filter(status='issued').count()
    maintenance_count   = Maintenance.objects.filter(
                            status__in=['pending', 'in_progress']).count()
    pending_count       = Booking.objects.filter(status='pending').count()

    # ── Chart 1: Equipment by Category (Pie) ──────────────────
    cat_data = Category.objects.annotate(
        eq_count=Count('equipment')
    ).filter(eq_count__gt=0).values_list('name', 'eq_count')

    cat_labels  = [row[0] for row in cat_data]
    cat_values  = [row[1] for row in cat_data]
    cat_colors  = [
        '#4f8ef7', '#22c55e', '#f59e0b', '#ef4444',
        '#a855f7', '#38bdf8', '#fb923c', '#84cc16',
    ]

    # ── Chart 2: Monthly Bookings — last 6 months (Line) ──────
    today  = timezone.now().date()
    months = []
    monthly_counts = []
    for i in range(5, -1, -1):
        # First day of month i months ago
        d = today.replace(day=1) - timedelta(days=i * 30)
        month_start = d.replace(day=1)
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1, day=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1, day=1)

        count = Booking.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lt=month_end
        ).count()

        months.append(month_start.strftime('%b %Y'))
        monthly_counts.append(count)

    # ── Chart 3: Top 5 Most Booked Equipment (Bar) ────────────
    top_eq = Booking.objects.values(
        'equipment__name'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:5]

    top_eq_labels = [row['equipment__name'][:20] for row in top_eq]
    top_eq_values = [row['total'] for row in top_eq]

    # ── Recent bookings ────────────────────────────────────────
    recent_bookings = Booking.objects.select_related(
        'requester', 'equipment'
    ).order_by('-created_at')[:8]

    # ── Overdue ────────────────────────────────────────────────
    overdue_count = Booking.objects.filter(
        status='issued',
        required_till__lt=today
    ).count()

    return {
        # Stats
        'total_equipment':     total_equipment,
        'available_equipment': available_equipment,
        'issued_count':        issued_count,
        'maintenance_count':   maintenance_count,
        'pending_count':       pending_count,
        'overdue_count':       overdue_count,
        'recent_bookings':     recent_bookings,

        # Chart data (JSON)
        'chart_cat_labels':   json.dumps(cat_labels),
        'chart_cat_values':   json.dumps(cat_values),
        'chart_cat_colors':   json.dumps(cat_colors[:len(cat_labels)]),

        'chart_month_labels': json.dumps(months),
        'chart_month_values': json.dumps(monthly_counts),

        'chart_top_labels':   json.dumps(top_eq_labels),
        'chart_top_values':   json.dumps(top_eq_values),
    }


# ─── Staff Context ────────────────────────────────────────────────────────────

def _staff_context(request):
    from bookings.models import Booking
    today = timezone.now().date()

    pending_bookings = Booking.objects.filter(
        status='pending'
    ).select_related('requester', 'equipment', 'equipment__lab').order_by('-created_at')

    issued_bookings  = Booking.objects.filter(
        status='issued'
    ).select_related('requester', 'equipment').order_by('required_till')

    overdue = issued_bookings.filter(required_till__lt=today)

    return {
        'pending_count':   pending_bookings.count(),
        'issued_count':    issued_bookings.count(),
        'overdue_count':   overdue.count(),
        'today_new':       Booking.objects.filter(created_at__date=today).count(),
        'pending_bookings': pending_bookings[:10],
        'issued_bookings':  issued_bookings[:8],
    }


# ─── Student/Faculty Context ──────────────────────────────────────────────────

def _student_context(request):
    from bookings.models import Booking
    from equipment.models import Equipment

    my_bookings = Booking.objects.filter(
        requester=request.user
    ).select_related('equipment').order_by('-created_at')

    featured_equipment = Equipment.objects.filter(
        status='available'
    ).select_related('category', 'lab')[:6]

    return {
        'active_count':        my_bookings.filter(status='issued').count(),
        'pending_count':       my_bookings.filter(status='pending').count(),
        'completed_count':     my_bookings.filter(status='completed').count(),
        'total_count':         my_bookings.count(),
        'recent_bookings':     my_bookings[:5],
        'featured_equipment':  featured_equipment,
    }


# ─── Reports Context ──────────────────────────────────────────────────────────

def _reports_context(request):
    from equipment.models import Equipment, Category, Lab
    from bookings.models import Booking, Maintenance
    from django.db.models import Sum

    today = timezone.now().date()

    # Equipment usage report
    equipment_usage = Equipment.objects.annotate(
        total_bookings=Count('bookings'),
        issued_now=Count('bookings', filter=Q(bookings__status='issued')),
    ).select_related('category', 'lab').order_by('-total_bookings')

    # Maintenance report
    maintenance_list = Maintenance.objects.select_related(
        'equipment', 'reported_by', 'resolved_by'
    ).order_by('-created_at')[:20]

    # Overdue returns
    overdue_list = Booking.objects.filter(
        status='issued',
        required_till__lt=today
    ).select_related('requester', 'equipment').order_by('required_till')

    # Summary stats
    total_bookings    = Booking.objects.count()
    completed_bookings = Booking.objects.filter(status='completed').count()
    active_maintenance = Maintenance.objects.filter(
                            status__in=['pending', 'in_progress']).count()

    return {
        'equipment_usage':     equipment_usage,
        'maintenance_list':    maintenance_list,
        'overdue_list':        overdue_list,
        'total_bookings':      total_bookings,
        'completed_bookings':  completed_bookings,
        'active_maintenance':  active_maintenance,
        'overdue_count':       overdue_list.count(),
    }
