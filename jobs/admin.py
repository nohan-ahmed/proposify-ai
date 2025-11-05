from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "job_type", "status", "queued_at", "started_at", "finished_at")
    list_filter = ("job_type", "status", "queued_at")
    search_fields = ("id", "user__username", "user__email")
    ordering = ("-queued_at",)
    readonly_fields = ("queued_at", "started_at", "finished_at")
    fieldsets = (
        (None, {
            "fields": ("user", "job_type", "status", "queued_at", "started_at", "finished_at")
        }),
        ("Result", {
            "fields": ("result_meta", "error", "attempts")
        }),
        ("LLM", {
            "fields": ("llm",)
        }),
        ("User Prompt", {
            "fields": ("user_prompt",)
        }),
    )
    

@admin.register(models.Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "job", "title", "visibility", "created_at", "updated_at")
    list_filter = ("visibility", "created_at", "updated_at")
    search_fields = ("id", "user__username", "user__email", "title")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
