from rest_framework import serializers # type: ignore
from .models import (
    Department,
    Staff,
    Patient,
    Appointment,  # Make sure this is imported
    Medicine,
    Prescription
)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'
        extra_kwargs = {
            'role': {'help_text': f"Available choices: {dict(Staff.ROLES)}"}
        }

    def validate_role(self, value):
        if value not in dict(Staff.ROLES):
            raise serializers.ValidationError(
                f"Invalid role. Choices are: {dict(Staff.ROLES)}"
            )
        return value

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'
