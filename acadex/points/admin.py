from django.contrib import admin
from .models import PointTransaction

@admin.register(PointTransaction)
class PointTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'points', 'point_type', 'created_at']
    list_filter = ['point_type', 'created_at']