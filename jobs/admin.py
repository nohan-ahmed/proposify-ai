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

    fieldsets = (
        (None, {
            "fields": ("user", "job", "title", "visibility", "created_at", "updated_at")
        }),
        ("LLM", {
            "fields": ("llm",)
        }),
        ("Prompt", {
            "fields": ("prompt", "language", "tone")
        }),
        ("Generated Text", {
            "fields": ("generated_text", "tokens_prompt", "tokens_completion", "tokens_total", "is_paid")
        }),
    )
    

@admin.register(models.BillingLog)
class BillingLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "proposal", "cost", "currency", "created_at")
    list_filter = ("currency", "created_at")
    search_fields = ("id", "user__username", "user__email", "proposal__title")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    fieldsets = (
        (None, {
            "fields": ("user", "proposal", "llm", "tokens_prompt", "tokens_completion", "cost", "currency", "created_at")
        }),
    )