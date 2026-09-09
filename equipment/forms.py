from django import forms
from .models import Equipment, Category, Lab


class EquipmentForm(forms.ModelForm):
    """Form to add or edit equipment."""

    class Meta:
        model  = Equipment
        fields = ['name', 'category', 'lab', 'description',
                  'quantity', 'available_quantity', 'purchase_date', 'image']
        widgets = {
            'name':               forms.TextInput(attrs={'placeholder': 'e.g., Arduino Uno'}),
            'description':        forms.Textarea(attrs={'rows': 3, 'placeholder': 'Brief description...'}),
            'quantity':           forms.NumberInput(attrs={'min': 1}),
            'available_quantity': forms.NumberInput(attrs={'min': 0}),
            'purchase_date':      forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned = super().clean()
        qty   = cleaned.get('quantity')
        avail = cleaned.get('available_quantity')
        if qty is not None and avail is not None:
            if avail > qty:
                self.add_error('available_quantity',
                               'Available quantity cannot exceed total quantity.')
        return cleaned


class CategoryForm(forms.ModelForm):
    class Meta:
        model  = Category
        fields = ['name', 'description']
        widgets = {
            'name':        forms.TextInput(attrs={'placeholder': 'e.g., Microcontroller'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }


class EquipmentFilterForm(forms.Form):
    """Search and filter form for equipment list."""
    q         = forms.CharField(required=False, widget=forms.TextInput(attrs={
                    'placeholder': 'Search by name or asset ID...'}))
    category  = forms.ModelChoiceField(queryset=Category.objects.all(),
                    required=False, empty_label='All Categories')
    lab       = forms.ModelChoiceField(queryset=Lab.objects.filter(is_active=True),
                    required=False, empty_label='All Labs')
    status    = forms.ChoiceField(choices=[('', 'All Status'),
                                           ('available',   'Available'),
                                           ('unavailable', 'Unavailable')],
                                  required=False)
