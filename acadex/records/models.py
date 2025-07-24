from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TestRecord(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='test_records'

    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_records'
    )

    subject = models.CharField(
        max_length=100
    )

    score = models.FloatField()

    max_score = models.FloatField(default=100)

    test_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-test_date']
    

    def __str__(self):
        return f"{self.student.username} - {self.subject}: {self.score}/{self.max_score}"