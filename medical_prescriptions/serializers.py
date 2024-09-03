from rest_framework import serializers
from .models import MedicalPrescription

class MedicalPrescriptionSerializer(serializers.ModelSerializer):
    medication_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True
    )
    
    class Meta:
        model = MedicalPrescription
        fields = ['id','doctor_id', 'patient_id', 'medication_ids', 'description', 'dose', 'date', 'prescription_file']