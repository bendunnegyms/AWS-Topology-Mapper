from django.shortcuts import render
from rest_framework.views import APIView 
from . models import *
from rest_framework.response import Response 
from .serializer import *

from to_frontend_format import ec2_instances_to_frontend_format
from describe_ec2_instances import ec2_api_details as ec2
from describe_sec_groups import security_group_api_details as secgroups

class Database_Instances(APIView):
    #request sent to /instances on load/reloading page
    def(self, request):
        print(request.text())
        instance_details = databases_to_frontend_format(secgroups(),databases())
        return Response(instance_details)

class Loadbalancer_Instances(APIView):
    def(self, request):
        print(request.text())
        instance_details = loadbalancers_to_frontend_format(secgroups(), loadbalancers())
        return Response(instance_details)