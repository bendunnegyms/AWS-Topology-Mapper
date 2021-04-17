from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from core.views import *

urlpatterns = [
    path("", index.as_view(), name="index"),
    path('admin/', admin.site.urls),
    path('wel/', EC2DataView.as_view(), name="something"),
    path('instances/', EC2_Instances.as_view(), name="instances"),
    path('NodeView', single_node.as_view(), name="Single Node"),
    path('GlobalView', entire_graph.as_view(), name="Global View"),
    path('SecurityGroups', security_groups.as_view(), name="Security Groups"),
    path('Ports', ports.as_view(), name="Ports")
    #path('loadbalancer_instances/', Loadbalancer_Instances.as_view(), name="loadbalancer_instances"),
    #path('database_instances/', Database_Instances.as_view(), name="database_instances")
]
