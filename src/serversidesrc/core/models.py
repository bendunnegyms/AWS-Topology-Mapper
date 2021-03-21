from django.db import models

class SecurityGroup(models.Model):
    group_name = models.CharField(max_length = 255)
    description = models.TextField()
    owner_id = models.IntegerField(default=0)
    group_id = models.CharField(max_length = 255)
    vpc_id = models.CharField(max_length = 255)

class IpPermissions(models.Model):
    from_port = models.IntegerField(default=0)
    ip_protocol = models.CharField(max_length = 255)
    to_port = models.IntegerField(default=0)
    security_group = models.ForeignKey(SecurityGroup, on_delete=models.CASCADE, related_name = 'ip_permissions', blank=True, null=True)

class IpRanges(models.Model):
    ip_range = models.CharField(max_length = 255)
    ip_permissions = models.ForeignKey(IpPermissions, on_delete=models.CASCADE, related_name = 'ip_ranges', blank=True, null=True)

class Ipv6Ranges(models.Model):
    ipv6_range = models.CharField(max_length = 255)
    ip_permissions = models.ForeignKey(IpPermissions, on_delete=models.CASCADE, related_name = 'ipv6_ranges', blank=True, null=True)

class PrefixListIds(models.Model):
    prefix_id = models.CharField(max_length = 255)
    ip_permissions = models.ForeignKey(IpPermissions, on_delete=models.CASCADE, related_name = 'prefix_list_ids', blank=True, null=True)

class UserIdGroupPairs(models.Model):
    group_id = models.CharField(max_length = 255)
    group_name = models.CharField(max_length = 255)
    user_id = models.IntegerField(default=0)
    permission = models.OneToOneField(IpPermissions, unique=True, on_delete=models.CASCADE, related_name='user_id_group_pairs', blank=True, null=True)

#some inputs only include egress information
class IpPermissionsEgress(models.Model):
    from_port = models.IntegerField(default=0)
    ip_protocol = models.CharField(max_length = 255)
    to_port = models.IntegerField(default=0)
    security_group = models.ForeignKey(SecurityGroup, on_delete=models.CASCADE, related_name = 'ip_permissions_egress', blank=True, null=True)
    
    def egress_url(URL):
        security_group = SecurityGroup.objects.get(id=1)
        output = "IpPermissionsEgressURL:" + URL + security_group.group_name
        return output

class IpRangesEgress(models.Model):
    ip_range = models.CharField(max_length = 255)
    ip_permissions = models.ForeignKey(IpPermissionsEgress, on_delete=models.CASCADE, related_name = 'ip_ranges_egress', blank=True, null=True)

class Ipv6RangesEgress(models.Model):
    ipv6_range = models.CharField(max_length = 255)
    ip_permissions = models.ForeignKey(IpPermissionsEgress, on_delete=models.CASCADE, related_name = 'ipv6_ranges', blank=True, null=True)

class PrefixListIdsEgress(models.Model):
    prefix_id = models.CharField(max_length = 255)
    ip_permissions = models.ForeignKey(IpPermissionsEgress, on_delete=models.CASCADE, related_name = 'prefix_list_ids_egress', blank=True, null=True)

class UserIdGroupPairsEgress(models.Model):
    group_id = models.CharField(max_length = 255)
    user_id = models.IntegerField(default=0)
    permissions_egress = models.OneToOneField(IpPermissionsEgress, unique=True, on_delete=models.CASCADE, related_name='user_id_group_pairs_egress', blank=True, null=True)

#Some data include a plethora of tags
class Tags(models.Model):
    key = models.CharField(max_length = 255)
    value = models.CharField(max_length = 255)
    security_group = models.ForeignKey(SecurityGroup, on_delete=models.CASCADE, related_name='tags', blank=True, null=True)

class EC2_Details(models.Model):
    name = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    security_group_id = models.IntegerField(default=0)
    