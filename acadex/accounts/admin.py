from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_teacher', 'points', 'streak_days']
    list_filter = ['is_teacher']