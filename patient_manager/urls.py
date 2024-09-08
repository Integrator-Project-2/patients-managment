from django.urls import path
from .views import AssociateDoctorPatientAPIView, DoctorPatientsListAPIView

urlpatterns = [
    path('associate-doctor-patient/', AssociateDoctorPatientAPIView.as_view(), name='associate-doctor-patient'),
    path('doctors/<int:doctor_id>/patients/', DoctorPatientsListAPIView.as_view(), name='doctor-patients-list')
]
