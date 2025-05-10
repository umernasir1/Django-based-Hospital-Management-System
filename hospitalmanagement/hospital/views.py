from pyexpat.errors import messages
from typing import Generic
from django.shortcuts import get_object_or_404, redirect, render  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework import generics
from django.urls import reverse_lazy # type: ignore
from django.views.generic import CreateView, UpdateView, ListView, DetailView # type: ignore
from rest_framework.response import Response  # type: ignore
from django.db.models import Q  # type: ignore
from rest_framework import generics # type: ignore
from django.shortcuts import get_object_or_404, redirect, render # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin # type: ignore
from hospital.forms import DepartmentForm, PatientForm,StaffForm,AppointmentForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView  # Added DeleteView
from .serializers import DepartmentSerializer
from .models import Department, Staff, Patient, Appointment, Medicine, Prescription
from .serializers import (
    DepartmentSerializer,
    StaffSerializer,
    PatientSerializer,
    AppointmentSerializer,
    MedicineSerializer,
    PrescriptionSerializer
)

# ------------------- Template Views -------------------

def dashboard(request):
    stats = {
        'department_count': Department.objects.count(),
        'patient_count': Patient.objects.count(),
        'staff_count': Staff.objects.count(),
        'appointment_count': Appointment.objects.count()
    }
    return render(request, 'dashboard.html', stats)


# ----- Department Views -----
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/list.html', {'departments': departments})

def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('departments-list')
    else:
        form = DepartmentForm()
    return render(request, 'departments/form.html', {'form': form})

def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('departments-list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'departments/form.html', {'form': form})

def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('departments-list')
    return render(request, 'departments/department_confirm_delete.html', {'department': department})

def department_detail(request, pk):
    department = get_object_or_404(Department, pk=pk)
    return render(request, 'departments/detail.html', {'department': department})
class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'departments/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Remove any references to head if they exist
        return context

# ----- Patient Views -----
class PatientListView(ListView):
    model = Patient
    template_name = 'patients/list.html'  # Changed to plural 'patients'
    context_object_name = 'patients'

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/form.html'  # Changed to plural
    success_url = reverse_lazy('patient-list')

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'patients/form.html'  # Changed to plural
    success_url = reverse_lazy('patient-list')


class DepartmentPartialUpdateView(generics.UpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    http_method_names = ['patch']  # Only allow PATCH
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    # This already supports GET, PUT, PATCH, DELETE
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'patients/detail.html', {'patient': patient})

def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient-list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})
# ------------------- API Views -------------------

class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
class DepartmentListView(ListView):
    model = Department
    template_name = 'departments/list.html'
    context_object_name = 'departments'

class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/form.html'
    success_url = reverse_lazy('department-list')

class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'departments/form.html'
    success_url = reverse_lazy('department-list')

class DepartmentDetailView(DetailView):
    model = Department
    template_name = 'departments/detail.html'

class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    template_name = 'departments/department_confirm_delete.html'
    success_url = reverse_lazy('department-list')

class StaffListView(LoginRequiredMixin, ListView):
    model = Staff
    template_name = 'staff/list.html'
    context_object_name = 'staff_list'
    paginate_by = 10

    def get_queryset(self):
        return Staff.objects.select_related('user', 'department').all()

class StaffListCreateView(generics.ListCreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class StaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class StaffCreateView(LoginRequiredMixin, CreateView):
    model = Staff
    form_class = StaffForm
    template_name = 'staff/form.html'
    success_url = reverse_lazy('staff-list')

    def form_valid(self, form):
        # Add any additional processing here
        return super().form_valid(form)

class StaffUpdateView(LoginRequiredMixin, UpdateView):
    model = Staff
    form_class = StaffForm
    template_name = 'staff/form.html'
    success_url = reverse_lazy('staff-list')

def staff_detail(request, pk):
    staff = get_object_or_404(Staff.objects.select_related('user', 'department'), pk=pk)
    return render(request, 'staff/detail.html', {'staff': staff})

def staff_delete(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.delete()
        return redirect('staff-list')
    return render(request, 'staff/staff_confirm_delete.html', {'staff': staff})
class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointments/list.html'
    context_object_name = 'appointments'
    
    def get_queryset(self):
        return super().get_queryset().select_related(
            'patient',
            'doctor',
            'doctor__user'
        )
class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/form.html'
    success_url = reverse_lazy('appointment-list')

class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/form.html'
    success_url = reverse_lazy('appointment-list')

def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(request, 'appointments/detail.html', {'appointment': appointment})

def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment-list')
    return render(request, 'appointments/confirm_delete.html', {'appointment': appointment})
class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filterset_fields = ['gender']
    search_fields = ['first_name', 'last_name', 'phone']

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class AppointmentListCreateView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filterset_fields = ['status', 'department']
    search_fields = ['patient__first_name', 'patient__last_name']

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class MedicineListCreateView(generics.ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    filterset_fields = ['category']
    search_fields = ['name', 'manufacturer']

class MedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class PrescriptionListCreateView(generics.ListCreateAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    filterset_fields = ['medicine', 'appointment']

class PrescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
def profile_view(request):
    return render(request, 'profile.html')

def custom_logout(request):
    # Optional: Add any pre-logout logic here
    if request.user.is_authenticated:
        print(f"User {request.user.username} is logging out")
    
    logout(request) # type: ignore
    
    messages.success(request, "You have been successfully logged out.")
    
    return redirect('home')   
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not user.check_password(old_password):
            return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'error': 'New passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)