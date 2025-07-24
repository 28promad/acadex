from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE
    )

    is_teacher = models.BooleanField(
        default=False
    )

    points = models.IntegerField(
        default=0
    )
    
    streak_days = models.IntegerField(
        default=0
    )

    last_activity = models.DateField(
        null=True,
        blank=True
    )


    def __str__(self):
        return f"{self.user.username} ({'Teacher' if self.is_teacher else 'Student'})"