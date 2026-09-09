from django.db import models
from django.conf import settings
from django.utils import timezone
from equipment.models import Equipment


# ─── BOOKING ───────────────────────────────────────────────────────────────────

def generate_booking_ref():
    """
    Auto-generate booking reference: BK-{YEAR}-{4-digit-seq}
    e.g., BK-2026-0001
    """
    year = timezone.now().year
    prefix = f"BK-{year}-"
    count = Booking.objects.filter(booking_ref__startswith=prefix).count()
    return f"{prefix}{str(count + 1).zfill(4)}"


class Booking(models.Model):
    """Tracks the full equipment rental request lifecycle."""

    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('approved',  'Approved'),
        ('rejected',  'Rejected'),
        ('issued',    'Issued'),
        ('completed', 'Completed'),
    ]

    # Reference
    booking_ref = models.CharField(max_length=20, unique=True, blank=True,
                                   help_text="Auto-generated: BK-2026-0001")

    # Who is requesting
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
        help_text="Student or Faculty who made the request"
    )

    # What is being booked
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE,
                                  related_name='bookings')
    quantity = models.PositiveIntegerField(default=1)

    # Dates
    request_date = models.DateField(auto_now_add=True)
    required_from = models.DateField()
    required_till = models.DateField()

    # Status & Approval
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                               default='pending')
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='approved_bookings',
        help_text="Staff or Admin who approved/rejected"
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    # Notes
    notes = models.TextField(blank=True, null=True,
                             help_text="Student's note/reason for request")
    rejection_reason = models.TextField(blank=True, null=True,
                                        help_text="Staff's reason for rejection")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-generate booking_ref on first save
        if not self.booking_ref:
            self.booking_ref = generate_booking_ref()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_ref} — {self.requester.username} → {self.equipment.name}"

    @property
    def is_overdue(self):
        """Check if this booking/return is overdue."""
        if self.status == 'issued':
            return timezone.now().date() > self.required_till
        return False

    class Meta:
        ordering = ['-created_at']


# ─── ISSUE LOG ─────────────────────────────────────────────────────────────────

class IssueLog(models.Model):
    """
    Tracks the physical issue and return of equipment for a booking.
    One IssueLog per Booking (created when equipment is issued).
    """

    CONDITION_CHOICES = [
        ('good',    'Good'),
        ('damaged', 'Damaged'),
        ('lost',    'Lost'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE,
                                   related_name='issue_log')

    # Issue details
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='issued_logs',
        help_text="Staff who issued the equipment"
    )
    issued_at = models.DateTimeField(auto_now_add=True)
    expected_return = models.DateField(help_text="= booking.required_till")

    # Return details (filled when equipment is returned)
    actual_return = models.DateTimeField(null=True, blank=True)
    returned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='received_returns',
        help_text="Staff who received the returned equipment"
    )
    condition_on_return = models.CharField(
        max_length=10, choices=CONDITION_CHOICES,
        null=True, blank=True
    )
    remarks = models.TextField(blank=True, null=True)

    @property
    def is_overdue(self):
        """True if returned after expected_return date."""
        if self.actual_return:
            return self.actual_return.date() > self.expected_return
        return False

    def __str__(self):
        return f"IssueLog for {self.booking.booking_ref}"

    class Meta:
        verbose_name = "Issue Log"
        verbose_name_plural = "Issue Logs"


# ─── MAINTENANCE ───────────────────────────────────────────────────────────────

class Maintenance(models.Model):
    """
    Created when equipment is returned in damaged or lost condition.
    Equipment available_quantity is NOT restored until this is resolved.
    """

    STATUS_CHOICES = [
        ('pending',     'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved',    'Resolved'),
    ]

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE,
                                  related_name='maintenance_records')
    issue_log = models.ForeignKey(IssueLog, on_delete=models.SET_NULL,
                                  null=True, blank=True,
                                  related_name='maintenance',
                                  help_text="Which return triggered this")
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True,
        related_name='reported_maintenance'
    )
    issue_description = models.TextField()
    quantity_affected = models.PositiveIntegerField(default=1,
                                                    help_text="How many units are damaged/lost")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES,
                               default='pending')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='resolved_maintenance'
    )
    resolution_notes = models.TextField(blank=True, null=True)

    def resolve(self, resolved_by_user, notes=""):
        """
        Mark maintenance as resolved.
        Restores available_quantity on the equipment.
        """
        from django.utils import timezone
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.resolved_by = resolved_by_user
        self.resolution_notes = notes
        self.save()

        # Restore stock
        eq = self.equipment
        eq.available_quantity += self.quantity_affected
        eq.save()

    def __str__(self):
        return f"Maintenance: {self.equipment.name} ({self.get_status_display()})"

    class Meta:
        ordering = ['-created_at']
