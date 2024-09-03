import base64
import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from .models import MedicalPrescription
from medical_prescriptions.serializers import MedicalPrescriptionSerializer
from medical_prescriptions.utils import generate_pdf

class MedicalPrescriptionCreateAPIView(APIView): 
    def post(self, request):
        serializer = MedicalPrescriptionSerializer(data=request.data)
        
        if serializer.is_valid():
            prescription = serializer.save()
            
            pdf_content = generate_pdf(serializer.data)
            
            prescription.prescription_file.save(
                f'prescription_{prescription.id}.pdf',
                ContentFile(pdf_content),
                save=True
            )

            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
            
            response_data = serializer.data
            response_data['prescription_pdf'] = pdf_base64
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientPrescriptionsAPIView(APIView):
    def get(self, request, patient_id):
        prescriptions = MedicalPrescription.objects.filter(patient_id=patient_id).order_by('-date')
        
        if prescriptions.exists():
            serializer = MedicalPrescriptionSerializer(prescriptions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No prescriptions found for this patient"}, status=status.HTTP_404_NOT_FOUND)
    
class PatientMedicationsAPIView(APIView):
    def get(self, request, patient_id):
        prescriptions = MedicalPrescription.objects.filter(patient_id=patient_id)
        
        if prescriptions.exists():
            medication_ids = []
            
            for prescription in prescriptions:
                medication_ids.extend(prescription.medication_ids)
                
            # remove duplicates
            medication_ids = list(set(medication_ids))
            
            medications = []
            medications_service_base_url = os.getenv('MEDICATIONS_SERVICE_BASE_API_URL')
            for medication_id in medication_ids:
                response = requests.get(f'{medications_service_base_url}/api/medications/{medication_id}/')
                
                if response.status_code == 200:
                    medications.append(response.json())
                else:
                    medications.append({
                        'id': medication_id,
                        'detail': 'not found',
                    })
                
            return Response({'medications': medications}, status=status.HTTP_200_OK)
        return Response({"detail": "No prescriptions found for this patient."}, status=status.HTTP_404_NOT_FOUND)
                
        
        
        
        
             
                
