from rest_framework import serializers 
from . models import *
  
class SecurityGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityGroup
        fields = ['group_name', 'description', 'owner_id', 'group_id', 'vpc_id']

class IpPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IpPermissions
        fields = ['from_port', 'ip_protocol', 'to_port']
        related_object = 'security_group' 

class IpRangesSerializer(serializers.ModelSerializer):
    class Meta:
        model = IpRanges
        fields = ['ip_range']
        related_object = 'ip_permissions'

class Ipv6RangesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ipv6Ranges
        fields = ['ipv6_range']
        related_object = 'ip_permissions'

class PrefixListIdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrefixListIds
        fields = ['prefix_id']
        related_object = 'ip_permissions'

class UserIdGroupPairsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIdGroupPairs
        fields = ['group_id', 'group_name', 'user_id']
        related_object = 'ip_permissions'

class IpPermissionEgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = IpPermissionEgress
        fields = ['from_port', 'ip_protocol', 'to_port']
        related_object = 'security_groups'

class IpRangesEgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = IpRangesEgress
        fields = ['ip_range']
        related_object = 'ip_permissions_egress'

class Ipv6RangesEgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ipv6RangesEgress
        fields = ['ipv6_range']
        related_object = 'ip_permissions_egress'

class PrefixListIdsEgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrefixListIdsEgress
        fields = ['prefix_id']
        related_object = 'ip_permissions_egress'

class UserIdGroupPairsEgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIdGroupPairsEgress
        fields = ['group_id', 'user_id']
        related_object = 'ip_permissions_egress'

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['key', 'value']
        related_object = 'security_group'


class EC2DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EC2_Details
        fields = ['name', 'description', 'security_group_id']