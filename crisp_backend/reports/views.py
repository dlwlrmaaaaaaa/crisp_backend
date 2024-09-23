import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, storage, firestore
from rest_framework.exceptions import NotFound
from rest_framework import generics, status
from rest_framework.response import Response
from users.models import Report, User  # Import your Report model and User model
from .serializers import ReportSerializer  # Import your serializer

cred = credentials.Certificate('C:/Users/ADMIN/Documents/crisp-5d09f-firebase-adminsdk-vl4cg-30e5cb1ca3.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'crisp-5d09f.appspot.com'
})

db = firestore.client()

class ReportView(generics.GenericAPIView):
    serializer_class = ReportSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Retrieve citizen instance based on user_id
            citizen = User.objects.get(id=request.data['user_id'])

            report_data = {
                'user_id': citizen.id,
                'image_path': request.data['image_path'],  # Initially set for local upload
                'type_of_report': request.data['type_of_report'],
                'report_description': request.data['report_description'],
                'longitude': request.data['longitude'],
                'latitude': request.data['latitude'],
                'upvote': 0,
                'status': "Pending",
                'report_date': datetime.now().isoformat()
            }

            # Upload the image to Firebase Storage
            image_name = os.path.basename(report_data['image_path'])
            bucket = storage.bucket()
            blob = bucket.blob(f'images/{image_name}')
            blob.upload_from_filename(report_data['image_path'])  # Upload the local file
            report_data['image_path'] = blob.public_url  # Get the public URL

            # Save report to Firestore
            db.collection('reports').add(report_data)

            # Save report to PostgreSQL
            report = Report(**report_data)
            report.save()

            return Response({"message": "Report saved"}, status=status.HTTP_201_CREATED)

        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
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
