from django.contrib import admin
from .models import Category, Lab, Equipment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'location')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('asset_id', 'name', 'category', 'lab',
                    'quantity', 'available_quantity', 'status', 'updated_at')
    list_filter = ('status', 'category', 'lab')
    search_fields = ('asset_id', 'name')
    readonly_fields = ('asset_id', 'qr_code', 'created_at', 'updated_at')
    ordering = ('asset_id',)

    fieldsets = (
        ('Identification', {
            'fields': ('asset_id', 'name', 'category', 'lab', 'description')
        }),
        ('Stock', {
            'fields': ('quantity', 'available_quantity', 'status')
        }),
        ('Details', {
            'fields': ('purchase_date', 'image', 'qr_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
