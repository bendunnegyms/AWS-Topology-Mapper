from django.shortcuts import render
from rest_framework.views import APIView 
from . models import *
from rest_framework.response import Response 
from .serializer import *

from to_frontend_format import ec2_instances_to_frontend_format
from describe_ec2_instances import ec2_api_details as ec2
from describe_sec_groups import security_group_api_details as secgroups

# Create your views here. 

class SecurityGroupView(APIView):
    serializer_class = SecurityGroupSerializer 
  
    def get(self, request): 
        security_groups = [ {"group_name": security_groups.group_name, 
            "description": security_groups.description, "owner_id": security_groups.owner_id,
            "group_id": security_groups.group_id, "vpc_id": security_groups.vpc_id}  
        for security_groups in SecurityGroup.objects.all()]
        print(security_groups) 
        return Response(security_groups) 
  
    def post(self, request): 
        print(request.data)
        serializer = SecurityGroupSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True): 
            serializer.save() 
            return  Response(serializer.data) 
    
  
class EC2DataView(APIView): 
    
    serializer_class = EC2DetailsSerializer 
  
    def get(self, request): 
        ec2_details = [ {"name": ec2_details.name,"description": ec2_details.description, "security_group_id": ec2_details.security_group_id}  
        for ec2_details in EC2_Details.objects.all()]
        print(ec2_details) 
        return Response(ec2_details) 
  
    def post(self, request): 
        print(request.data)
        serializer = EC2DetailsSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True): 
            serializer.save() 
            return  Response(serializer.data) 

class EC2_Instances(APIView):

    # Request sent to /instances on load/reloading page
    def get(self, request):
        print(request.text())
        instance_details = ec2_instances_to_frontend_format(secgroups(),ec2())
        return Response(instance_details)