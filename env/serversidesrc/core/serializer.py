from rest_framework import serializers 
from . models import *
  
class EC2DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EC2_Details
        fields = ['name', 'description', 'security_group_id']