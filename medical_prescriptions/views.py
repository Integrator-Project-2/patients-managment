import base64
import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from medical_prescriptions.models import MedicalPrescription
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
        
        if not prescriptions.exists():
            return Response({"detail": "No prescriptions found for this patient."}, status=status.HTTP_404_NOT_FOUND)
        
        medication_ids = []
        for prescription in prescriptions:
            medication_ids.extend(prescription.medication_ids)

        medication_ids = list(set(medication_ids))
        
        medications_service_base_url = os.getenv('MEDICATIONS_SERVICE_BASE_API_URL')
        if not medications_service_base_url:
            return Response({"detail": "Medications service base URL not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        medications = []
        name_query = request.query_params.get('name', None)

        for medication_id in medication_ids:
            url = f'{medications_service_base_url}/api/medications/{medication_id}/'
            if name_query:
                url += f'?name={name_query}'
            
            try:
                response = requests.get(url)
                response.raise_for_status()
                medication_data = response.json()
                
                if 'name' in medication_data:
                    medications.append(medication_data)
                else:
                    medications.append({
                        'id': medication_id,
                        'detail': 'Name field not found in medication response',
                    })
            
            except requests.RequestException as e:
                medications.append({
                    'id': medication_id,
                    'detail': f'Error fetching medication: {str(e)}',
                })
        
        if name_query:
            medications = [
                medication for medication in medications if 'name' in medication and name_query.lower() in medication['name'].lower()
            ]
        
        return Response({'medications': medications}, status=status.HTTP_200_OK)