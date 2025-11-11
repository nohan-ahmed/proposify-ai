from django.db import models


class ProviderChoices(models.TextChoices):
    OPENAI = "openai", "OpenAI"
    HUGGINGFACE = "huggingface", "HuggingFace"
    GEMINI = "gemini", "Gemini"
    CLAUDE = "claud", "Claude"
    CUSTOM = "custom", "Custom"