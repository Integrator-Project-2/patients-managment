from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MedicalPrescription, AuditLog

@receiver(post_save, sender=MedicalPrescription)
def log_prescription_save(sender, instance, created, **kwargs):
    if created:
        AuditLog.objects.create(
            doctor_id = instance.doctor_id,
            prescription_id = instance.id,
            operation='created'
        )