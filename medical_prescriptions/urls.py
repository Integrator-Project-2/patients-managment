from django.urls import path
from .import views

urlpatterns = [
    path('medical-prescriptions/', views.MedicalPrescriptionCreateAPIView.as_view(), name='medical-prescription-create'),
    path('prescriptions/patient/<int:patient_id>/', views.PatientPrescriptionsAPIView.as_view(), name='patient-prescriptions'),
    path('medications/patient/<int:patient_id>/', views.PatientMedicationsAPIView.as_view(), name='patient-medications'),
]