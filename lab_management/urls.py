"""
Root URL Configuration — BCA_29 Lab Equipment Rental & Management System
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    # Root → redirect to dashboard (will redirect to login if not authenticated)
    path("", lambda request: redirect("dashboard:index"), name="home"),

    # Django Admin
    path("admin/", admin.site.urls),

    # Our apps
    path("", include("accounts.urls")),
    path("", include("equipment.urls")),
    path("", include("bookings.urls")),
    path("", include("dashboard.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = 'django.views.defaults.page_not_found'
handler403 = 'django.views.defaults.permission_denied'
handler500 = 'django.views.defaults.server_error'
