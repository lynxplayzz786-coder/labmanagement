from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    path('equipment/',              views.equipment_list,   name='list'),
    path('equipment/add/',          views.equipment_add,    name='add'),
    path('equipment/<int:pk>/',     views.equipment_detail, name='detail'),
    path('equipment/<int:pk>/edit/',views.equipment_edit,   name='edit'),
    path('equipment/<int:pk>/delete/', views.equipment_delete, name='delete'),
    path('equipment/<int:pk>/qr/', views.equipment_qr,     name='qr'),
]
