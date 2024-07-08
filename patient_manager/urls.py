from django.urls import path
from .views import AssociateDoctorPatientAPIView

urlpatterns = [
    path('associate-doctor-patient/', AssociateDoctorPatientAPIView.as_view(), name='associate-doctor-patient'),
]
