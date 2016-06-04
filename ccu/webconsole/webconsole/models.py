from django.db import models
from django.conf import settings
from django.utils import timezone as tz
import uuid

# Create your models here.
class Appliance(models.Model):
	'''
	Repersenting a appliance
	'''
	id		= models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
	name		= models.CharField(max_length=100)

class Command(models.Model):
	'''
	Repersenting a supporting command
	'''
	id		= models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
	appliance	= models.ForeignKey(Appliance, on_delete=models.CASCADE)
	name		= models.CharField(max_length=100)

class Parameter(models.Model):
	'''
	Repersenting a command parameter
	'''
	id		= models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
	command		= models.ForeignKey(Command, on_delete=models.CASCADE)
	name		= models.CharField(max_length=100)
	typ		= models.CharField(max_length=50,default='string')
	defval		= models.CharField(max_length=100,blank=True,null=True)

class Permission(models.Model):
	'''
	Declare which user can execute which command. It can be volatiled by the user.is_superuser and user.is_staff
	'''
	user		= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	command		= models.ForeignKey(Command, on_delete=models.CASCADE)
	effdate		= models.DateTimeField(default=tz.now)
	expdate		= models.DateTimeField(null=True,blank=True)
