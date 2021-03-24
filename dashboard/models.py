from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone
from datetime import date
import datetime


class profile(models.Model):
    GENRE_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    birth_date = models.DateField(auto_now=False, blank= True,auto_now_add=False,null=True)
    genre = models.CharField(max_length=1, choices=GENRE_CHOICES,null=True)
    profile1 = models.ImageField(upload_to='images/', default='static/assets/img/bg5.jpg',null=True, blank=True)
    bgprofile = models.ImageField(upload_to='images/', default='static/assets/img/bg5.jpg',null=True, blank=True)
    address = models.CharField(max_length=1000,null=True)
    locatity = models.CharField(max_length=30,null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)


    def get_absolute_url(self):
        return reverse("accounts:profile_detail")
    
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)        

class Task(models.Model):
    task_name = models.CharField(max_length=255)
    task_desc = models.TextField(blank=True)
    task_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    task_taker = models.CharField(max_length=255, blank=True)
    time_created = models.DateTimeField(default=timezone.now)
    time_taken = models.DateTimeField(blank=True, null=True)
    time_done = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.task_name}'
    

