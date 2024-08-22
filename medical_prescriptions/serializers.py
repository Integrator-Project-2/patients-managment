from rest_framework import serializers
from .models import MedicalPrescription

class MedicalPrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalPrescription
        fields = ['doctor_id', 'patient_id', 'medication_id', 'description', 'dose']