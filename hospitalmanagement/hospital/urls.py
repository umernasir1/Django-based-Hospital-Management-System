from django.urls import path # type: ignore
from django.contrib.auth import views as auth_views # type: ignore
from rest_framework.authtoken.views import obtain_auth_token # type: ignore
from rest_framework.authtoken.views import obtain_auth_token
from .views import ChangePasswordView
from . import views
from .views import (
    AppointmentListView, ChangePasswordView, DepartmentListCreateView, DepartmentDetailView, DepartmentPartialUpdateView,
    StaffListCreateView, StaffDetailView,
    PatientListCreateView, PatientDetailView,
    AppointmentListCreateView, AppointmentDetailView,
    MedicineListCreateView, MedicineDetailView,
    PrescriptionListCreateView, PrescriptionDetailView,
    PatientListView, PatientCreateView, PatientUpdateView,
    StaffListView, StaffCreateView, StaffUpdateView,StaffListCreateView, StaffDetailView, appointment_detail, # Add these
  # Added missing imports
)

urlpatterns = [
     path('', views.dashboard, name='dashboard'),  
    path('api-token-auth/', obtain_auth_token),
    path('departments/', views.department_list, name='departments-list'),
    path('departments/create/', views.department_create, name='departments-create'),
    path('departments/<int:pk>/', views.department_detail, name='departments-detail'),
    path('departments/<int:pk>/update/', views.department_update, name='departments-update'),
    path('departments/<int:pk>/delete/', views.department_delete, name='departments-delete'),

    path('patients/', PatientListView.as_view(), name='patient-list'),
    path('patients/new/', PatientCreateView.as_view(), name='patient-create'),
    path('patients/<int:pk>/', views.patient_detail, name='patient-detail'),
    path('patients/<int:pk>/edit/', PatientUpdateView.as_view(), name='patient-update'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient-delete'),
    
    path('staff/', views.StaffListView.as_view(), name='staff-list'),
    path('staff/create/', views.StaffCreateView.as_view(), name='staff-create'),
    path('staff/<int:pk>/', views.staff_detail, name='staff-detail'),
    path('staff/<int:pk>/update/', views.StaffUpdateView.as_view(), name='staff-update'),
    path('staff/<int:pk>/delete/', views.staff_delete, name='staff-delete'),  
      
     path('appointments/', AppointmentListView.as_view(), name='appointment-list'),
     path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),    path('appointments/create/', views.AppointmentCreateView.as_view(), name='appointment-create'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment-detail'),
    path('appointments/<int:pk>/update/', views.AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment-delete'),

    # API URLs
    path('api/departments/', DepartmentListCreateView.as_view(), name='api-department-list'),
    path('api/departments/<int:pk>/', DepartmentDetailView.as_view(), name='api-department-detail'),
    path('api/staff/', StaffListCreateView.as_view(), name='api-staff-list'),
    path('api/staff/<int:pk>/', StaffDetailView.as_view(), name='api-staff-detail'),
    path('api/patients/', PatientListCreateView.as_view(), name='api-patient-list'),
    path('api/patients/<int:pk>/', PatientDetailView.as_view(), name='api-patient-detail'),
    path('api/appointments/', AppointmentListCreateView.as_view(), name='api-appointment-list'),
    path('api/appointments/<int:pk>/', AppointmentDetailView.as_view(), name='api-appointment-detail'),
    path('api/medicines/', MedicineListCreateView.as_view(), name='api-medicine-list'),
    path('api/medicines/<int:pk>/', MedicineDetailView.as_view(), name='api-medicine-detail'),
    path('api/prescriptions/', PrescriptionListCreateView.as_view(), name='api-prescription-list'),
    path('api/prescriptions/<int:pk>/', PrescriptionDetailView.as_view(), name='api-prescription-detail'),
    path('profile/', auth_views.PasswordChangeView.as_view(), name='profile'),
    path('api-token-auth/', obtain_auth_token),
    path('api/password/change/', ChangePasswordView.as_view(), name='api-password-change'),
    path('api/departments/<int:pk>/patch/', DepartmentPartialUpdateView.as_view(), name='api-department-partial-update'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
 
]