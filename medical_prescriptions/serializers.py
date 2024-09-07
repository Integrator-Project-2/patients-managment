import base64
from rest_framework import serializers
from .models import MedicalPrescription

class MedicalPrescriptionSerializer(serializers.ModelSerializer):
    medication_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True
    )
    prescription_pdf = serializers.SerializerMethodField()
    
    class Meta:
        model = MedicalPrescription
        fields = ['id', 'doctor_id', 'patient_id', 'medication_ids', 'description', 'dose', 'date', 'prescription_file','prescription_pdf']
        
    def get_prescription_pdf(self, obj):
        """Método para obter o PDF da prescrição como base64, se disponível."""
        if obj.prescription_file:
            with obj.prescription_file.open('rb') as pdf_file:
                pdf_content = pdf_file.read()
                return base64.b64encode(pdf_content).decode('utf-8')
        return None