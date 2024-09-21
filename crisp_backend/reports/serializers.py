from rest_framework import serializers
from users.models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['user_id',
                    'image_path',
                    'type_of_report',
                    'report_description',
                    'longitude',
                    'latitude',
                    'upvote',
                    'status'] 

    
  

