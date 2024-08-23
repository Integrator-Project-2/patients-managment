from django.urls import path
from .views import AssociateDoctorPatientAPIView, PatientPrescriptionsAPIView, PatientMedicationsAPIView

urlpatterns = [
    path('associate-doctor-patient/', AssociateDoctorPatientAPIView.as_view(), name='associate-doctor-patient'),
    path('prescriptions/patient/<int:patient_id>/', PatientPrescriptionsAPIView.as_view(), name='patient-prescriptions'),
    path('medications/patient/<int:patient_id>/', PatientMedicationsAPIView.as_view(), name='patient-medications'),
]
