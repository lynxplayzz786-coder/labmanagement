from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django import forms
from accounts.decorators import login_required_custom, role_required
from .models import Booking, IssueLog, Maintenance
from .forms import BookingForm, ReturnForm, RejectionForm
from equipment.models import Equipment


# ═══════════════════════════════════════════════════════════════
# STUDENT / FACULTY VIEWS
# ═══════════════════════════════════════════════════════════════

@login_required_custom
def my_bookings(request):
    """Student/Faculty — view own bookings."""
    bookings = Booking.objects.filter(
        requester=request.user
    ).select_related('equipment', 'equipment__category', 'equipment__lab').order_by('-created_at')

    # Filter by status if provided
    status = request.GET.get('status', '')
    if status:
        bookings = bookings.filter(status=status)

    return render(request, 'bookings/my_bookings.html', {
        'bookings':        bookings,
        'status_filter':   status,
        'STATUS_CHOICES':  Booking.STATUS_CHOICES,
    })


@login_required_custom
def new_booking(request):
    """Student/Faculty — submit a new booking request."""
    if not request.user.can_request_booking:
        messages.error(request, "Only students and faculty can request bookings.")
        return redirect('dashboard:index')

    equipment_id = request.GET.get('equipment')
    form = BookingForm(request.POST or None, equipment_id=equipment_id)

    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        booking.requester = request.user
        booking.status    = 'pending'
        booking.save()

        messages.success(
            request,
            f"Booking request submitted! Reference: {booking.booking_ref}. "
            f"Please wait for staff approval."
        )
        return redirect('bookings:my_bookings')

    return render(request, 'bookings/booking_form.html', {
        'form':           form,
        'preselected_id': equipment_id,
        'today':          timezone.now().date().isoformat(),
    })


# ═══════════════════════════════════════════════════════════════
# STAFF / ADMIN VIEWS
# ═══════════════════════════════════════════════════════════════

@role_required('admin', 'staff')
def manage_bookings(request):
    """Staff/Admin — view and manage all bookings."""
    status  = request.GET.get('status', 'pending')
    bookings = Booking.objects.select_related(
        'requester', 'equipment', 'equipment__category', 'equipment__lab'
    ).order_by('-created_at')

    if status:
        bookings = bookings.filter(status=status)

    # Count badges for each status
    counts = {
        'pending':   Booking.objects.filter(status='pending').count(),
        'approved':  Booking.objects.filter(status='approved').count(),
        'issued':    Booking.objects.filter(status='issued').count(),
        'completed': Booking.objects.filter(status='completed').count(),
        'rejected':  Booking.objects.filter(status='rejected').count(),
    }

    return render(request, 'bookings/manage_bookings.html', {
        'bookings':      bookings,
        'status_filter': status,
        'counts':        counts,
    })


@role_required('admin', 'staff')
def approve_booking(request, pk):
    """Staff/Admin — approve a pending booking."""
    booking = get_object_or_404(Booking, pk=pk, status='pending')

    if request.method == 'POST':
        # Re-check availability at time of approval (Business Rule 1)
        eq = booking.equipment
        if booking.quantity > eq.available_quantity:
            messages.error(
                request,
                f"Cannot approve: only {eq.available_quantity} units available, "
                f"but {booking.quantity} requested."
            )
            return redirect('bookings:manage_bookings')

        booking.status      = 'approved'
        booking.approved_by = request.user
        booking.approved_at = timezone.now()
        booking.save()

        messages.success(
            request,
            f"Booking {booking.booking_ref} approved! "
            f"You can now issue the equipment to {booking.requester.get_full_name() or booking.requester.username}."
        )

    return redirect('bookings:manage_bookings')


@role_required('admin', 'staff')
def reject_booking(request, pk):
    """Staff/Admin — reject a pending booking with a reason."""
    booking = get_object_or_404(Booking, pk=pk, status='pending')
    form    = RejectionForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        booking.status           = 'rejected'
        booking.approved_by      = request.user
        booking.approved_at      = timezone.now()
        booking.rejection_reason = form.cleaned_data['rejection_reason']
        booking.save()

        messages.success(request, f"Booking {booking.booking_ref} rejected.")
        return redirect('bookings:manage_bookings')

    return render(request, 'bookings/reject_form.html', {
        'booking': booking,
        'form':    form,
    })


@role_required('admin', 'staff')
def issue_equipment(request, pk):
    """Staff — issue approved equipment. Decreases available_quantity."""
    booking = get_object_or_404(Booking, pk=pk, status='approved')

    if request.method == 'POST':
        eq = booking.equipment

        # Final availability check (Business Rule 4)
        if booking.quantity > eq.available_quantity:
            messages.error(
                request,
                f"Cannot issue: only {eq.available_quantity} units now available."
            )
            return redirect('bookings:manage_bookings')

        # Decrease stock
        eq.available_quantity -= booking.quantity
        eq.save()

        # Create IssueLog
        IssueLog.objects.create(
            booking         = booking,
            issued_by       = request.user,
            expected_return = booking.required_till,
        )

        # Update booking status
        booking.status = 'issued'
        booking.save()

        messages.success(
            request,
            f"Equipment issued for {booking.booking_ref}. "
            f"Stock updated: {eq.name} → {eq.available_quantity} available."
        )

    return redirect('bookings:manage_bookings')


@role_required('admin', 'staff')
def process_return(request, pk):
    """Staff — process equipment return + condition check."""
    booking = get_object_or_404(Booking, pk=pk, status='issued')
    form    = ReturnForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        condition   = form.cleaned_data['condition_on_return']
        remarks     = form.cleaned_data.get('remarks', '')
        issue_desc  = form.cleaned_data.get('issue_description', '')

        # Update IssueLog
        issue_log                    = booking.issue_log
        issue_log.actual_return      = timezone.now()
        issue_log.returned_to        = request.user
        issue_log.condition_on_return = condition
        issue_log.remarks            = remarks
        issue_log.save()

        eq = booking.equipment

        if condition == 'good':
            # Business Rule 5: Restore stock
            eq.available_quantity += booking.quantity
            eq.save()
            booking.status = 'completed'
            booking.save()
            messages.success(
                request,
                f"Return processed for {booking.booking_ref}. "
                f"Stock restored: {eq.name} → {eq.available_quantity} available."
            )

        else:
            # Business Rule 6: Damaged/Lost — create maintenance, do NOT restore stock
            Maintenance.objects.create(
                equipment          = eq,
                issue_log          = issue_log,
                reported_by        = request.user,
                issue_description  = issue_desc or f"{condition.title()} — {remarks}",
                quantity_affected  = booking.quantity,
                status             = 'pending',
            )
            booking.status = 'completed'
            booking.save()
            messages.warning(
                request,
                f"Return processed for {booking.booking_ref}. "
                f"Equipment marked as {condition}. Maintenance record created. "
                f"Stock NOT restored until maintenance is resolved."
            )

    return render(request, 'bookings/return_form.html', {
        'booking': booking,
        'form':    form,
    })


# ═══════════════════════════════════════════════════════════════
# MAINTENANCE MANAGEMENT
# ═══════════════════════════════════════════════════════════════

@role_required('admin', 'staff')
def maintenance_list(request):
    """Staff/Admin — view all maintenance records."""
    status_filter = request.GET.get('status', '')

    records = Maintenance.objects.select_related(
        'equipment', 'equipment__lab', 'reported_by', 'resolved_by'
    ).order_by('-created_at')

    if status_filter:
        records = records.filter(status=status_filter)

    counts = {
        'pending':     Maintenance.objects.filter(status='pending').count(),
        'in_progress': Maintenance.objects.filter(status='in_progress').count(),
        'resolved':    Maintenance.objects.filter(status='resolved').count(),
    }

    return render(request, 'bookings/maintenance_list.html', {
        'records':       records,
        'status_filter': status_filter,
        'counts':        counts,
    })


class MaintenanceResolveForm(forms.Form):
    resolution_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Describe how the issue was resolved (repair, replacement, write-off)…'
        }),
        label="Resolution Notes"
    )
    status = forms.ChoiceField(choices=[
        ('in_progress', 'Mark as In Progress'),
        ('resolved',    'Mark as Resolved (restores stock)'),
    ])


@role_required('admin', 'staff')
def maintenance_resolve(request, pk):
    """Admin/Staff — update or resolve a maintenance record."""
    from django import forms as dj_forms

    record = get_object_or_404(Maintenance, pk=pk)

    class ResolveForm(dj_forms.Form):
        resolution_notes = dj_forms.CharField(
            widget=dj_forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'How was it resolved? (repair, write-off, replaced…)'
            }),
            label="Resolution Notes", required=True
        )
        new_status = dj_forms.ChoiceField(
            choices=[
                ('in_progress', '🔧 Mark as In Progress'),
                ('resolved',    '✅ Mark as Resolved (restores stock)'),
            ],
            label="Update Status"
        )

    form = ResolveForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        new_status = form.cleaned_data['new_status']
        notes      = form.cleaned_data['resolution_notes']

        if new_status == 'resolved':
            record.resolve(resolved_by_user=request.user, notes=notes)
            eq = record.equipment
            messages.success(
                request,
                f"Maintenance resolved! {eq.name} stock restored by {record.quantity_affected} unit(s). "
                f"New available: {eq.available_quantity}."
            )
        else:
            record.status = 'in_progress'
            record.resolution_notes = notes
            record.save()
            messages.info(request, f"Maintenance marked as In Progress.")

        return redirect('bookings:maintenance_list')

    return render(request, 'bookings/maintenance_resolve.html', {
        'record': record,
        'form':   form,
    })
