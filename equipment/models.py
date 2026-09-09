from django.db import models
from django.conf import settings


# ─── CATEGORY ──────────────────────────────────────────────────────────────────
class Category(models.Model):
    """Equipment category — e.g., Microcontroller, Networking, Sensor"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']


# ─── LAB ───────────────────────────────────────────────────────────────────────
class Lab(models.Model):
    """Physical lab in the college — e.g., IoT Lab, Computer Lab 1"""

    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200, blank=True, null=True,
                                help_text="e.g., Block B, Room 201")
    capacity = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


# ─── EQUIPMENT ─────────────────────────────────────────────────────────────────

# Category code mapping for asset_id generation
CATEGORY_CODES = {
    'arduino': 'ARD',
    'raspberry pi': 'RPi',
    'oscilloscope': 'OSC',
    'multimeter': 'MLT',
    'networking': 'NET',
    'projector': 'PRJ',
    'sensor': 'SEN',
    'cable': 'CBL',
}


def get_category_code(category_name):
    """Return 3-letter code for a category name."""
    name_lower = category_name.lower()
    for key, code in CATEGORY_CODES.items():
        if key in name_lower:
            return code
    # Default: first 3 letters of category name, uppercased
    return category_name[:3].upper()


def generate_asset_id(category):
    """
    Auto-generate asset_id in format: LAB-{CAT_CODE}-{3-digit-seq}
    e.g., LAB-ARD-001, LAB-ARD-002
    """
    code = get_category_code(category.name)
    prefix = f"LAB-{code}-"
    # Count existing equipment with same category code
    count = Equipment.objects.filter(asset_id__startswith=prefix).count()
    return f"{prefix}{str(count + 1).zfill(3)}"


class Equipment(models.Model):
    """Core equipment model — tracks all lab equipment."""

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]

    # Identification
    asset_id = models.CharField(max_length=20, unique=True, blank=True,
                                help_text="Auto-generated: LAB-ARD-001")
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name='equipment')
    lab = models.ForeignKey(Lab, on_delete=models.PROTECT,
                            related_name='equipment')
    description = models.TextField(blank=True, null=True)

    # Stock
    quantity = models.PositiveIntegerField(default=1,
                                           help_text="Total units owned")
    available_quantity = models.PositiveIntegerField(default=1,
                                                     help_text="Currently available")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES,
                               default='available')

    # Details
    purchase_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='equipment/', blank=True, null=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-generate asset_id on first save
        if not self.asset_id:
            self.asset_id = generate_asset_id(self.category)

        # Auto-set status based on available_quantity
        if self.available_quantity == 0:
            self.status = 'unavailable'
        else:
            self.status = 'available'

        super().save(*args, **kwargs)

        # Generate QR code after save (needs pk to exist)
        if not self.qr_code:
            self._generate_qr_code()

    def _generate_qr_code(self):
        """Generate QR code image for this equipment."""
        import qrcode
        from io import BytesIO
        from django.core.files.base import ContentFile

        qr_data = (
            f"Asset ID: {self.asset_id}\n"
            f"Name: {self.name}\n"
            f"Lab: {self.lab.name}\n"
            f"Status: {self.get_status_display()}"
        )

        qr_img = qrcode.make(qr_data)
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        filename = f"qr_{self.asset_id}.png"

        # Save without triggering save() again
        Equipment.objects.filter(pk=self.pk).update(
            qr_code=f"qrcodes/{filename}"
        )
        # Write actual file
        from django.core.files.storage import default_storage
        default_storage.save(f"qrcodes/{filename}", ContentFile(buffer.getvalue()))

    def __str__(self):
        return f"{self.asset_id} — {self.name}"

    class Meta:
        ordering = ['asset_id']
        verbose_name_plural = "Equipment"
