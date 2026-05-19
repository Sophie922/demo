from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create-application/', views.create_application_view, name='create_application'),
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
]