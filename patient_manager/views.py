import os
import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from medical_prescriptions.models import MedicalPrescription
from medical_prescriptions.serializers import MedicalPrescriptionSerializer
from .models import DoctorPatientAssociation
class AssociateDoctorPatientAPIView(APIView):
    
    def post(self, request, format=None):
        doctor_id = request.data.get('doctor_id')
        patient_id = request.data.get('patient_id')
        
        base_api_url = settings.USER_SERVICES_BASE_API_URL
        
        doctor_microservice_url = f'{base_api_url}api/doctors/'
        patient_microservice_url = f'{base_api_url}api/pacients/'
                
        try:
            doctor_response = requests.get(doctor_microservice_url + f'{doctor_id}/')
            patient_response = requests.get(patient_microservice_url + f'{patient_id}/')
            doctor_data = doctor_response.json()
            
            patient_data = patient_response.json()
            
            if doctor_response.status_code == 200 and patient_response.status_code == 200:
                association = DoctorPatientAssociation.objects.create(
                    doctor_id=doctor_data['id'],
                    patient_id=patient_data['id']
                )
                
                return Response({'success': 'Vínculo criado com sucesso!'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Erro ao buscar médico ou paciente.'}, status=status.HTTP_404_NOT_FOUND)
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Erro de conexão com o microserviço de médicos ou pacientes.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PatientPrescriptionsAPIView(APIView):
    def get(self, request, patient_id):
        prescriptions = MedicalPrescription.objects.filter(patient_id=patient_id)
        
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
                
        
        
        
        
             
                
