from django.utils.timezone import localtime
from django.db import models
from django.contrib.postgres.fields import ArrayField

class MedicalPrescription(models.Model):
    doctor_id = models.IntegerField()
    patient_id = models.IntegerField()
    medication_ids = ArrayField(models.IntegerField(), default=list)
    description = models.TextField()
    prescription_file = models.FileField(upload_to='prescriptions/', null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    
class AuditLog(models.Model):
    doctor_id = models.IntegerField()
    prescription_id = models.IntegerField()
    operation = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
