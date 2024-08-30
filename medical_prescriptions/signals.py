import requests
from django.db.models.signals import post_save
from django.dispatch import receiver

from patient_manager.models import DoctorPatientAssociation
from .models import MedicalPrescription, AuditLog

def get_expo_push_token_from_microservice(patient_id):
    try:
        response = requests.get(f'http://127.0.0.1:8001/api/pacients/{patient_id}/')
        response_data = response.json()
        return response_data.get('expo_push_token')
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar o token do paciente: {e}")
        return None

def send_push_notification(token, title, message):
    payload = {
        'to': token,
        'sound': 'default',
        'title': title,
        'body': message,
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post('https://exp.host/--/api/v2/push/send', json=payload, headers=headers)
    if response.status_code != 200:
        print(f"Erro ao enviar notificação: {response.text}")

def get_doctor_name_from_service(doctor_id):
    url = f'http://localhost:8001/api/doctors/{doctor_id}/'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        doctor_name = data.get('user', {}).get('name')
        return doctor_name
    except requests.exceptions.RequestException as e:
        return None

@receiver(post_save, sender=MedicalPrescription)
def log_prescription_save(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(
            doctor_id=instance.doctor_id,
            prescription_id=instance.id,
            operation='created'
        )
        
        # buscar o token do paciente do microserviço de pacientes
        expo_push_token = get_expo_push_token_from_microservice(instance.patient_id)
        
        # enviar a notificação se o token estiver disponível
        if expo_push_token:
            send_push_notification(
                token=expo_push_token,
                title="Nova Prescrição",
                message=f"Você tem uma nova prescrição adicionada"
            )


@receiver(post_save, sender=DoctorPatientAssociation)
def doctor_association_notify(sender, instance, created, **kwargs):
    if created:
        expo_push_token = get_expo_push_token_from_microservice(instance.patient_id)
        doctor_name = get_doctor_name_from_service(instance.doctor_id)
        
        if expo_push_token:
            send_push_notification(
                token=expo_push_token,
                title="Novo vínculo",
                message=f"Dr. {doctor_name} te adicionou!"
            )
