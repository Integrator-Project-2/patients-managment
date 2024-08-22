from django.db import models

class MedicalPrescription(models.Model):
    doctor_id = models.IntegerField()
    patient_id = models.IntegerField()
    medication_id = models.IntegerField()
    description = models.TextField()
    dose = models.CharField(max_length=255)
    prescription_file = models.FileField(upload_to='prescriptions/', null=True, blank=True)
    
class AuditLog(models.Model):
    doctor_id = models.IntegerField()
    prescription_id = models.IntegerField()
    operation = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
