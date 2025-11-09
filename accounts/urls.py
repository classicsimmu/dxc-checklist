from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('doer-dashboard/', views.doer_dashboard, name='doer_dashboard'),
    path('staff/users/', views.user_list_view, name='user_list'),  # 👈 new
path('staff/users/add/', views.add_user_view, name='add_user'),  # 👈 new
path('staff/users/edit/<int:user_id>/', views.edit_user_view, name='edit_user'),
path('staff/users/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),
path('staff/users/reset-password/<int:user_id>/', views.reset_password_view, name='reset_password'),

]
