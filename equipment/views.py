from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from accounts.decorators import login_required_custom, role_required
from .models import Equipment, Category, Lab
from .forms import EquipmentForm, EquipmentFilterForm


@login_required_custom
def equipment_list(request):
    """
    Equipment list with search, filter, and pagination.
    Accessible to all authenticated users.
    """
    form = EquipmentFilterForm(request.GET or None)
    qs   = Equipment.objects.select_related('category', 'lab').all()

    # Apply filters
    if form.is_valid():
        q        = form.cleaned_data.get('q')
        category = form.cleaned_data.get('category')
        lab      = form.cleaned_data.get('lab')
        status   = form.cleaned_data.get('status')

        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(asset_id__icontains=q)
        if category:
            qs = qs.filter(category=category)
        if lab:
            qs = qs.filter(lab=lab)
        if status:
            qs = qs.filter(status=status)

    # Paginate — 12 per page (nice for grid)
    paginator = Paginator(qs.order_by('asset_id'), 12)
    page      = request.GET.get('page', 1)
    equipment = paginator.get_page(page)

    return render(request, 'equipment/list.html', {
        'equipment': equipment,
        'form':      form,
        'total':     qs.count(),
    })


@login_required_custom
def equipment_detail(request, pk):
    """Equipment detail page — shows full info + booking history."""
    eq = get_object_or_404(Equipment.objects.select_related('category', 'lab'), pk=pk)
    recent_bookings = eq.bookings.select_related('requester').order_by('-created_at')[:5]

    return render(request, 'equipment/detail.html', {
        'eq':              eq,
        'recent_bookings': recent_bookings,
    })


@role_required('admin')
def equipment_add(request):
    """Add new equipment — admin only."""
    form = EquipmentForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        eq = form.save()
        messages.success(request, f"Equipment '{eq.name}' added successfully! Asset ID: {eq.asset_id}")
        return redirect('equipment:detail', pk=eq.pk)

    return render(request, 'equipment/add_edit.html', {
        'form':   form,
        'action': 'Add',
    })


@role_required('admin')
def equipment_edit(request, pk):
    """Edit existing equipment — admin only."""
    eq   = get_object_or_404(Equipment, pk=pk)
    form = EquipmentForm(request.POST or None, request.FILES or None, instance=eq)

    if request.method == 'POST' and form.is_valid():
        eq = form.save()
        messages.success(request, f"Equipment '{eq.name}' updated successfully!")
        return redirect('equipment:detail', pk=eq.pk)

    return render(request, 'equipment/add_edit.html', {
        'form':   form,
        'eq':     eq,
        'action': 'Edit',
    })


@role_required('admin')
def equipment_delete(request, pk):
    """Delete equipment — admin only. POST only."""
    eq = get_object_or_404(Equipment, pk=pk)

    if request.method == 'POST':
        # Safety check — don't delete if it has active bookings
        active = eq.bookings.filter(status__in=['pending', 'approved', 'issued']).exists()
        if active:
            messages.error(request, f"Cannot delete '{eq.name}' — it has active bookings.")
            return redirect('equipment:detail', pk=eq.pk)

        name = eq.name
        eq.delete()
        messages.success(request, f"Equipment '{name}' deleted successfully.")
        return redirect('equipment:list')

    return redirect('equipment:detail', pk=pk)


@login_required_custom
def equipment_qr(request, pk):
    """Display QR code for an equipment item."""
    eq = get_object_or_404(Equipment, pk=pk)

    # Regenerate QR if missing
    if not eq.qr_code:
        eq._generate_qr_code()
        eq.refresh_from_db()

    return render(request, 'equipment/qr.html', {'eq': eq})
