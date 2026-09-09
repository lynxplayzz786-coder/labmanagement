from django.contrib import admin
from .models import Booking, IssueLog, Maintenance


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_ref', 'requester', 'equipment', 'quantity',
                    'required_from', 'required_till', 'status', 'created_at')
    list_filter = ('status', 'required_from')
    search_fields = ('booking_ref', 'requester__username', 'equipment__name',
                     'equipment__asset_id')
    readonly_fields = ('booking_ref', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Reference', {
            'fields': ('booking_ref', 'requester', 'equipment', 'quantity')
        }),
        ('Dates', {
            'fields': ('request_date', 'required_from', 'required_till')
        }),
        ('Status', {
            'fields': ('status', 'approved_by', 'approved_at',
                       'notes', 'rejection_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(IssueLog)
class IssueLogAdmin(admin.ModelAdmin):
    list_display = ('booking', 'issued_by', 'issued_at',
                    'expected_return', 'actual_return', 'condition_on_return')
    list_filter = ('condition_on_return',)
    search_fields = ('booking__booking_ref',)
    readonly_fields = ('issued_at',)


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'quantity_affected', 'status',
                    'reported_by', 'created_at', 'resolved_at')
    list_filter = ('status',)
    search_fields = ('equipment__name', 'equipment__asset_id')
    readonly_fields = ('created_at',)
