from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('generate/<int:vendor_id>/', views.generate_code, name='generate_code'),
]
