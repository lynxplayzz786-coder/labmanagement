from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('bookings/',                   views.my_bookings,      name='my_bookings'),
    path('bookings/new/',               views.new_booking,      name='new_booking'),
    path('bookings/manage/',            views.manage_bookings,  name='manage_bookings'),
    path('bookings/<int:pk>/approve/',  views.approve_booking,   name='approve_booking'),
    path('bookings/<int:pk>/reject/',   views.reject_booking,    name='reject_booking'),
    path('bookings/<int:pk>/issue/',    views.issue_equipment,   name='issue_equipment'),
    path('bookings/<int:pk>/return/',   views.process_return,    name='process_return'),

    # Maintenance
    path('maintenance/',                views.maintenance_list,  name='maintenance_list'),
    path('maintenance/<int:pk>/resolve/', views.maintenance_resolve, name='maintenance_resolve'),
]
