import os
import requests
import base64
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from medical_prescriptions.models import MedicalPrescription
from medical_prescriptions.serializers import MedicalPrescriptionSerializer
from .models import DoctorPatientAssociation
from django.conf import settings

class AssociateDoctorPatientAPIView(APIView):
    
    def post(self, request, format=None):
        doctor_id = request.data.get('doctor_id')
        patient_id = request.data.get('patient_id')
        
        if DoctorPatientAssociation.objects.filter(doctor_id=doctor_id, patient_id=patient_id).exists():
            return Response({'message': 'Esse vínculo já existe.'}, status=status.HTTP_200_OK)
                
        try:
            association = DoctorPatientAssociation.objects.create(
                doctor_id=doctor_id,
                patient_id=patient_id
            )
            
            return Response({'success': 'Vínculo criado com sucesso!'}, status=status.HTTP_201_CREATED)
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Erro de conexão com o microserviço de médicos ou pacientes.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DoctorPatientsListAPIView(APIView):
    
    def get(self, request, doctor_id, format=None):
        associations = DoctorPatientAssociation.objects.filter(doctor_id=doctor_id)
        
        patient_ids = associations.values_list('patient_id', flat=True)
        
        print("patient_ids: ", list(patient_ids))
        
        if not patient_ids:
            return Response({"error": "No patients found for this doctor."}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            url = f"{settings.USER_SERVICE_BASE_API_URL}/pacients/search-by-ids/"
            
            print('url: ', url)
            
            response = requests.post(url, json={"patient_ids": list(patient_ids)})
            
            if response.status_code == 200:
                patients_data = response.json()
                return Response(patients_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to fetch patient data from user-service."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except requests.exceptions.RequestException as e:
            return Response({"error": "Error connecting to user-service."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PatientPrescriptionsAPIView(APIView):
    def get(self, request, patient_id):
        prescriptions = MedicalPrescription.objects.filter(patient_id=patient_id)
        
        if prescriptions.exists():
            response_data = []
            for prescription in prescriptions:
                serializer = MedicalPrescriptionSerializer(prescription)
                
                # Adiciona o campo prescription_pdf no dicionário do serializer
                prescription_data = serializer.data
                
                if prescription.prescription_file:
                    with prescription.prescription_file.open('rb') as pdf_file:
                        pdf_content = pdf_file.read()
                        pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
                        prescription_data['prescription_pdf'] = pdf_base64
                else:
                    prescription_data['prescription_pdf'] = None

                response_data.append(prescription_data)

            return Response(response_data, status=status.HTTP_200_OK)
        
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
                    continue
                
            return Response({'medications': medications}, status=status.HTTP_200_OK)
        return Response({"detail": "No prescriptions found for this patient."}, status=status.HTTP_404_NOT_FOUND)
                
        
        
        
        
             
                
