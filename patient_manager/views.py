import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
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
                
                
