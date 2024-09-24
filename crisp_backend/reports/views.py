import os
from datetime import datetime
from django.contrib.auth.models import User
from firebase_admin import credentials, storage, firestore
from rest_framework.exceptions import NotFound
from rest_framework import generics, status
from rest_framework.response import Response
from users.models import Report, Citizen  # Import your Report model and User model
from .serializers import ReportSerializer  # Import your serializer
from crisp_backend.firebase import db, bucket
from rest_framework.permissions import AllowAny
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid

class ReportView(generics.GenericAPIView):
    serializer_class = ReportSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                # Fetching the user (citizen) by user_id
                citizen = Citizen.objects.get(id=request.data['user_id'])
                image_path_string = ''
                # Preparing report data
                report_data = {
                    'user_id': citizen.id,                   
                    'type_of_report': request.data['type_of_report'],
                    'report_description': request.data['report_description'],
                    'longitude': request.data['longitude'],
                    'latitude': request.data['latitude'],
                    'upvote': 0,
                    'status': "Pending",
                    'report_date': datetime.now().isoformat()
                }

                # Check if an image was uploaded
                if 'image' in request.FILES:
                    image_file = request.FILES['image']
                    image_name = str(uuid.uuid4())  # Generate unique image name

                    # Save the image to a temporary path
                    temp_image_path = default_storage.save(f'temporary_path/{image_name}', ContentFile(image_file.read()))

                    # Get a reference to the Firebase storage bucket
                    bucket = storage.bucket()

                    # Create a blob and upload the file to Firebase
                    image_blob = bucket.blob(f'images_report/{image_name}')
                    image_blob.upload_from_filename(temp_image_path, content_type=image_file.content_type)

                    # Make the image publicly accessible
                    image_blob.make_public()

                    # Add the image URL to report data
                    image_path_string = image_blob.public_url

                # Add the report to Firestore
                __added = db.collection('reports').add(report_data)
                report = Report(
                    user_id=citizen,
                    image_path=image_path_string,
                    type_of_report=request.data['type_of_report'],
                    report_description=request.data['report_description'],
                    longitude=request.data['longitude'],
                    latitude=request.data['latitude'],
                    upvote=0,
                    status="Pending",
                    report_date=datetime.now()
                     )
                report.save()
                # Respond with success message
                return Response({"message": "Report saved"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"errr": serializer.errors}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            raise NotFound(detail="User not found.")
    
    

    def put(self, request, *args, **kwargs):
        report = self.get_queryset().get(pk=kwargs['pk'])
        serializer = self.get_serializer(report, data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            report = self.get_queryset().get(pk=kwargs['pk'])
            report.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Report.DoesNotExist:
            raise NotFound(detail="Report not found.")
