from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PointTransaction(models.Model):
    POINT_TYPES = [
        ('study', 'Study Session'),
        ('quiz', 'Quiz Participation'),
        ('test', 'Test Score'),
        ('streak', 'Streak bonus'),
        ('imporvement', 'Improvement bonus'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    points = models.IntegerField()

    point_type = models.CharField(
        max_length=20,
        choices=POINT_TYPES
    )

    description = models.CharField(
        max_length=200
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"{self.user.username} - {self.points} points ({self.point_type})"