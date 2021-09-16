from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

# Create your models here.

class signup(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contact = models.CharField(max_length=10)
    branch = models.CharField(max_length=30)
    role = models.CharField(max_length=30)

    def __str__(self):
        return self.user.username

class notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    branch = models.CharField(max_length=30)
    uploadingnotes = models.FileField(upload_to='media/files/')
    date = models.DateField()
    filetype = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Room(models.Model):
    name = models.CharField(max_length=1000)

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)

class notification(models.Model):
    url = models.URLField(null=True)
    msg = models.CharField(max_length=100)
    date = models.DateField(default=datetime.now)

class contactus(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    msg = models.CharField(max_length=300)
