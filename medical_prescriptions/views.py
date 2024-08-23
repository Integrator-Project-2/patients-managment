import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
from .models import MedicalPrescription
from medical_prescriptions.serializers import MedicalPrescriptionSerializer
from medical_prescriptions.utils import generate_pdf

class MedicalPrescriptionCreateAPIView(APIView): 
    def post(self, request):
        serializer = MedicalPrescriptionSerializer(data=request.data)
        
        if serializer.is_valid():
            prescription = serializer.save()
            
            pdf_content = generate_pdf(serializer.data)
            
            prescription.prescription_file.save(
                f'prescription_{prescription.id}.pdf',
                ContentFile(pdf_content),
                save=True
            )

            pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
            
            response_data = serializer.data
            response_data['prescription_pdf'] = pdf_base64
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
