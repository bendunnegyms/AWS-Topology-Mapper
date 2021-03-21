from rest_framework import serializers, fields
from . models import *
  
class SecurityGroupSerializer(serializers.ModelSerializer):
    #ip_permissions_egress = IpPermissionsEgressSerializer(many=True, read_only=True)
    #ip_permissions = IpPermissionsSerializer(many=True, read_only=True)
    #tags = TagsSerializer(many=True, read_only=True)

    #data = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = SecurityGroup
        fields = '__ALL__'

    #Be able to update data
    #def update(self, request, *args, **kwargs):
    #    instance = self.get_object()
    #    serializer = ProfileSerializer(
    #    instance=instance,
    #    data=request.data
    #    )
    #    serializer.is_valid(raise_exception=True)
    #    serializer.save()
    #    return Response(serializer.data)

class IpPermissionsSerializer(serializers.ModelSerializer):
    #ip_ranges = IpRangesSerializer(many=True, read_only=True)
    #ipv6_ranges = Ipv6RangesSerializer(many=True, read_only=True)
    #prefix_list_ids = PrefixListIdsSerializer(many=True, read_only=True)
    #user_id_group_pairs = UserIdGroupPairsSerializer(many=True, read_only=True)
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

class IpPermissionsEgressSerializer(serializers.ModelSerializer):

    #ip_ranges_egress = IpRangesEgressSerializer(many=True, read_only=True)
    #ipv6_ranges_egress = Ipv6RangesEgressSerializer(many=True, read_only=True)
    #prefix_list_ids_egress = PrefixListIdsEgressSerializer(many=True, read_only=True)
    #user_id_group_pairs_egress = UserIdGroupPairsEgressSerializer(many=True, read_only=True)
    class Meta:
        model = IpPermissionsEgress
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
