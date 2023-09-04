from django.db import models

# Create your models here.
import datetime
from django.contrib.auth.models import User
class ForecastScenario(models.Model):
    title=models.CharField(max_length=50)
class Position(models.Model):
    title=models.CharField(max_length=100)
class Forecast(models.Model):
    userID=models.ForeignKey(User,on_delete=models.CASCADE)
    insertedBy=models.ForeignKey(User,on_delete=models.CASCADE,related_name="insertedBy")
    period=models.DateField()
    scenario=models.ForeignKey(ForecastScenario,on_delete=models.CASCADE,default=1)
    amount=models.CharField(max_length=20)
    createdAt=models.DateField(null=True)
    updatedAt=models.DateField()
class UserDetails(models.Model):
    userID=models.OneToOneField(User,on_delete=models.CASCADE)
    position=models.ForeignKey(Position,on_delete=models.CASCADE)
