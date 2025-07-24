from django.contrib import admin
from .models import TestRecord

@admin.register(TestRecord)
class TestRecordAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'score', 'test_date']
    list_filter = ['subject', 'test_date']