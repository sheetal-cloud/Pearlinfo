from django.contrib import admin
from django.contrib.auth.models import User
from .models import profile,Task

admin.site.register(profile)
admin.site.register(Task)