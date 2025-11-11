from huggingface_hub import InferenceClient
from django.conf import settings


def run_huggingface_model(model_name: str, prompt: str, max_new_tokens: int = 400, temperature: float = 0.7):
    client = InferenceClient(
        model_name, 
        token=settings.HUGGINGFACE_TOKEN
    )

    messages = [{"role": "user", "content": prompt}]
    result = client.chat_completion(
        model=model_name,  # Add this parameter
        messages=messages,
        max_tokens=max_new_tokens,
        temperature=temperature
    )

    return {
        "text": result.choices[0].message.content,
        "tokens_prompt": result.usage.prompt_tokens,
        "tokens_completion": result.usage.completion_tokens,
        "tokens_total": result.usage.total_tokens,
        "cost": 0.0
    }
