from rest_framework import serializers
from users.models import Report


class ReportSerializer(serializers.ModelSerializer):
    image_path = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = Report
        fields = [
            'user_id',
            'image_path',
            'type_of_report',
            'report_description',
            'longitude',
            'latitude',
            'upvote',
            'status',
            'report_date'
        ]

        def validate_image_path(self, value):
            if value and not isinstance(value, str):
                raise serializers.ValidationError("Image path must be a valid string.")
            return value

        # def validate_longitude(self, value):
        #     # Ensure the longitude is within acceptable range
        #     if value < -180 or value > 180:
        #         raise serializers.ValidationError("Invalid longitude value.")
        #     return value

        # def validate_latitude(self, value):
        #     # Ensure the latitude is within acceptable range
        #     if value < -90 or value > 90:
        #         raise serializers.ValidationError("Invalid latitude value.")
        #     return value 

    
  

