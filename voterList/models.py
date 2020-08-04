from django.db import models

class VoterRegistration(models.Model):
    '''Model to store VOter Registration Details'''
    Name = models.CharField(max_length=200, null=False)
    Address = models.CharField(max_length=200, null=False)
    DOB = models.DateField()
    state = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    pin = models.CharField(max_length=12, null=False)
    citizenship = models.BooleanField(null=False)
    age = models.BooleanField(null=False)
    Contact = models.CharField(max_length=12, null=False,unique=True)
    image = models.ImageField(upload_to = "images/")