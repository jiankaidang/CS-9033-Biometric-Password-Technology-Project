from django.db import models

# Create your models here.
class User(models.Model):
  uid=models.IntegerField(primary_key=True)
  username=models.CharField(max_length=50,unique=True)
  email=models.EmailField(max_length=255,unique=True)  
  def __unicode__(self):
    return self.username
  
class Piece(models.Model):
  piece_id=models.IntegerField(primary_key=True)
  signature=models.TextField(null=True)
  user=models.ForeignKey('User',)
  def __unicode__(self):
    return self.piece_id
  
class Service(models.Model):
  service_id=models.IntegerField(primary_key=True)
  service_name=models.CharField(max_length=50,unique=True)
  register_time=models.DateTimeField()
  auth_code=models.CharField(max_length=50,unique=True)
  
class Binding(models.Model):
  binding_id=models.IntegerField(primary_key=True)
  service_uid=models.IntegerField()
  binding_time=models.DateTimeField()
  piece=models.ForeignKey('Piece')
  service=models.ForeignKey('Service')
  
class Verify(models.Model):
  verify_id=models.IntegerField(primary_key=True)
  binding=models.ForeignKey('Binding')
  timestamp=models.DateTimeField()
  attempt_time=models.SmallIntegerField(default=0)
  
  
  
  