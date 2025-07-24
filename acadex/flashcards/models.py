from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Flashcard(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject}: {self.question[:50]}..."
    


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    correct = models.BooleanField()
    attempted_at = models.DateTimeField(auto_now_add=True)