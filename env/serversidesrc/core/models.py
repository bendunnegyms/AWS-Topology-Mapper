from django.db import models

# Create your models here.

class EC2_Details(models.Model):
    name = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    security_group_id = models.IntegerField(default=0)
    