from django.db import models
from django.contrib.auth.models import User  
from datetime import date


class Task(models.Model):
    name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    date=models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return self.name
