from django.apps import AppConfig


class MedicalPrescriptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medical_prescriptions'
    
    def ready(self):
        import medical_prescriptions.signals
