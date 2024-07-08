from django.db import models

class DoctorPatientAssociation(models.Model):
    doctor_id = models.IntegerField()
    patient_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['doctor_id', 'patient_id']
