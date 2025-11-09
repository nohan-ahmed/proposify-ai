from celery import shared_task
from django.utils import timezone
from .models import Proposal, BillingLog
from .prompts import generate_proposal_prompt
from .hf_inference import run_model

@shared_task
def process_proposal_async(proposal_id):
    proposal = Proposal.objects.get(id=proposal_id)
    job = proposal.job

    try:
        job.status = "running"
        job.started_at = timezone.now()
        job.save()
        
        system_prompt = generate_proposal_prompt(proposal)
        ai_result = run_model(system_prompt)
        
        proposal.generated_text = ai_result["text"]
        proposal.tokens_prompt = ai_result["tokens_prompt"]
        proposal.tokens_completion = ai_result["tokens_completion"]
        proposal.tokens_total = ai_result["tokens_total"]
        proposal.save()

        BillingLog.objects.create(
            user=proposal.user,
            proposal=proposal,
            llm=proposal.llm,
            tokens_prompt=proposal.tokens_prompt,
            tokens_completion=proposal.tokens_completion,
            cost=ai_result["cost"],
        )

        job.result_meta = ai_result
        job.status = "completed"
        job.finished_at = timezone.now()
        job.save()

    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        job.finished_at = timezone.now()
        job.save()
