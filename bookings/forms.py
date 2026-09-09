from django import forms
from django.utils import timezone
from .models import Booking
from equipment.models import Equipment


class BookingForm(forms.ModelForm):
    """Form for students/faculty to request equipment booking."""

    class Meta:
        model  = Booking
        fields = ['equipment', 'quantity', 'required_from', 'required_till', 'notes']
        widgets = {
            'required_from': forms.DateInput(attrs={'type': 'date'}),
            'required_till': forms.DateInput(attrs={'type': 'date'}),
            'notes':         forms.Textarea(attrs={
                                'rows': 3,
                                'placeholder': 'Reason for booking, purpose, project name…'
                             }),
        }

    def __init__(self, *args, **kwargs):
        # Accept optional pre-selected equipment
        equipment_id = kwargs.pop('equipment_id', None)
        super().__init__(*args, **kwargs)

        # Only show available equipment
        self.fields['equipment'].queryset = Equipment.objects.filter(
            status='available'
        ).select_related('category', 'lab')
        self.fields['equipment'].label_from_instance = lambda obj: \
            f"{obj.asset_id} — {obj.name} (Available: {obj.available_quantity})"

        if equipment_id:
            try:
                self.initial['equipment'] = Equipment.objects.get(pk=equipment_id)
            except Equipment.DoesNotExist:
                pass

    def clean(self):
        cleaned       = super().clean()
        equipment     = cleaned.get('equipment')
        quantity      = cleaned.get('quantity')
        req_from      = cleaned.get('required_from')
        req_till      = cleaned.get('required_till')
        today         = timezone.now().date()

        # Date validation
        if req_from and req_from < today:
            self.add_error('required_from', 'Required-from date cannot be in the past.')

        if req_from and req_till and req_till < req_from:
            self.add_error('required_till', 'Return date must be after the start date.')

        # Quantity vs available check (Business Rule 2)
        if equipment and quantity:
            if quantity > equipment.available_quantity:
                self.add_error(
                    'quantity',
                    f"Only {equipment.available_quantity} unit(s) available. "
                    f"You requested {quantity}."
                )
            if quantity < 1:
                self.add_error('quantity', 'Quantity must be at least 1.')

        return cleaned


class ReturnForm(forms.Form):
    """Form for staff to process equipment return with condition check."""

    CONDITION_CHOICES = [
        ('good',    'Good — Equipment is in perfect condition'),
        ('damaged', 'Damaged — Equipment has damage'),
        ('lost',    'Lost — Equipment cannot be found'),
    ]

    condition_on_return = forms.ChoiceField(
        choices   = CONDITION_CHOICES,
        widget    = forms.RadioSelect,
        label     = "Equipment Condition on Return"
    )
    remarks = forms.CharField(
        required = False,
        widget   = forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Any notes about the return condition…'
        }),
        label = "Staff Remarks (optional)"
    )

    # Only shown when damaged/lost
    issue_description = forms.CharField(
        required = False,
        widget   = forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Describe the damage or loss…'
        }),
        label = "Damage/Loss Description"
    )

    def clean(self):
        cleaned   = super().clean()
        condition = cleaned.get('condition_on_return')
        desc      = cleaned.get('issue_description')

        if condition in ['damaged', 'lost'] and not desc:
            self.add_error('issue_description',
                           'Please describe the damage or loss.')
        return cleaned


class RejectionForm(forms.Form):
    """Form for staff/admin to reject a booking with a reason."""
    rejection_reason = forms.CharField(
        widget = forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Reason for rejection (visible to student)…'
        }),
        label = "Rejection Reason"
    )
