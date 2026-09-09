from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds a 'role' field to distinguish Admin, Staff, Faculty, and Student.
    """

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Lab Staff'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student',
        help_text="User role determines access permissions."
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    enrollment_no = models.CharField(
        max_length=20, blank=True, null=True,
        help_text="Only for students."
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    # ─── Role helper properties ────────────────────────────────────────────────
    @property
    def is_admin_user(self):
        return self.role == 'admin'

    @property
    def is_staff_user(self):
        return self.role == 'staff'

    @property
    def is_faculty(self):
        return self.role == 'faculty'

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def can_request_booking(self):
        """Students and Faculty can request bookings."""
        return self.role in ['student', 'faculty']

    @property
    def can_manage_bookings(self):
        """Staff and Admin can approve/reject/issue/return."""
        return self.role in ['staff', 'admin']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
