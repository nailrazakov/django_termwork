from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.admin import ModelAdmin

from mailing.models import Attempt


@admin.register(Attempt)
class AttemptAdmin(ModelAdmin):
    list_display = ["status", "server_response", "mailing", "created_at"]
    list_filter = (
        "status",
        "server_response",
        "created_at",
    )
    search_fields = ("status", "server_response", "created_at", "mailing")