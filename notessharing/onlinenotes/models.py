from django.db import models
from django.contrib.auth.models import User

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
    uploadingnotes = models.FileField()
    filetype = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
