from .serializers import ReportSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import Report
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from crisp_backend.firebase import *
# from firebase_admin import firestore
# from firebase_admin import db
from datetime import datetime

# db = firestore.client()

class ReportView(generics.GenericAPIView):
    serializer_class = ReportSerializer
    permission_classes = [AllowAny] #papalitan to ng isAuthenticated for test purposes lang ang AllowAny

    def get_queryset(self):
        return Report.objects.all()
    
    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            report = self.get_queryset().get(pk=kwargs['pk'])
            serializer = report.get_serializer(report)
            return Response(serializer.data)
        else:
            reports = self.get_queryset()
            serializer = self.get_serializer(reports, many=True)
            return Response(serializer.data)
        
    def post(self, request, *args, **kwargs ):
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid()
        if valid:
            report_data = {
                'user_id': request.data['user_id'],
                'image_path': request.data['image_path'],
                'type_of_report': request.data['type_of_report'],
                'report_description': request.data['report_description'],
                'longitude': request.data['longitude'],
                'latitude': request.data['latitude'],
                'upvote': 0,
                'status': "Pending",
                'report_date': datetime.now().isoformat()
             }
        try:
            db.collection('reports').add(report_data)
            print("Report added to Firebase:", report_data)
            report = Report(
                user_id=request.data['user_id'],
                image_path=request.data['image_path'],
                type_of_report=request.data['type_of_report'],
                report_description=request.data['report_description'],
                longitude=request.data['longitude'],
                latitude=request.data['latitude'],
            )
            report.save()  
            return Response({"message": "Report saved"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error saving report:", e)
            return Response({"error": "Failed to save report"}, status=status.HTTP_400_BAD_REQUEST)
        
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


    
    


