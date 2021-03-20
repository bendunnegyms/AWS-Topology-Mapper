from django.db import models

class SecurtiyGroup(models.Model):
    group_name = models.CharField(max_length = 255)
    description = models.TextField()
    owner_id = models.IntegerField(default=0)
    group_id = models.CharField(max_length = 255)
    vpc_id = models.CharField(max_length = 255)

class IpPermissions(models.Model):
    from_port = models.IntegerField(default=0)
    ip_protocol = models.CharField(max_length = 255)
    to_port = models.IntegerField(default=0)
    security_group = models.ForeignKey(SecurityGroup, unique=True, on_delete=models.CASCADE)

class IpRanges(Models.Model):
    ip_range = models.CharField(max_length = 255)
    ip_permissions = models.ForeignKey(IpPermissions, related_name = 'IpRanges')

class Ipv6Ranges(Models.Model):
    ipv6_range = models.CharField(max_length = 255)
    ip_permissions = models.ForeignKey(IpPermissions, related_name = 'Ipv6Ranges')

class PrefixListIds(Models.Model):
    prefix_id = models.CharField(max_length = 255)
    ip_permissions = models.ForeignKey(IpPermissions, related_name = 'PrefixListIds')

class UserIdGroupPairs(models.Model):
    group_id = models.CharField(max_length = 255)
    group_name = models.CharField(max_length = 255)
    user_id = models.IntegerField(default=0)
    permission = models.OneToOneField(IpPermissions)

class IpPermissionEgress(models.Model):
    from_port = models.IntegerField(default=0)
    ip_protocol = models.CharField(max_length = 255)
    to_port = models.IntegerField(default=0)
    security_group = models.ForeignKey(SecurityGroup, unique=True, on_delete=models.CASCADE)

class IpRangesEgress(Models.Model):
    ip_range = models.CharField(max_length = 255)
    ip_permissions = models.ForeignKey(IpPermissionEgress, related_name = 'IpRanges')

class Ipv6RangesEgress(Models.Model):
    ipv6_range = models.CharField(max_length = 255)
    ip_permissions = models.ForeignKey(IpPermissionEgress, related_name = 'Ipv6Ranges')

class PrefixListIdsEgress(Models.Model):
    prefix_id = models.CharField(max_length = 255)
    ip_permissions = models.ForeignKey(IpPermissionEgress, related_name = 'PrefixListIds')

class UserIdGroupPairsEgress(models.Model):
    group_id = models.CharField(max_length = 255)
    user_id = models.IntegerField(default=0)
    permissions_egress = models.OneToOneField(IpPermissionEgress)

class Tags(models.Model):
    key = models.CharField(max_length = 255)
    value = models.CharField(max_length = 255)
    security_group = models.ForeignKey(SecurityGroup, unique=True, on_delete=models.CASCADE)

class EC2_Details(models.Model):
    name = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    security_group_id = models.IntegerField(default=0)
    