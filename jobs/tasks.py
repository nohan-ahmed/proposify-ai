from celery import shared_task
from django.utils import timezone
from .models import Proposal, BillingLog
from .prompts import generate_proposal_prompt
from llm_models.ai_services import run_huggingface_model

@shared_task
def process_proposal_async(proposal_id):
    # Get proposal
    proposal = Proposal.objects.get(id=proposal_id)
    # Get job
    job = proposal.job
    
    # Check if job is already running
    if job.status == "running":
        return None
    
    try:
        # Update job
        job.status = "running"
        job.started_at = timezone.now()
        job.save()
        
        # Generate prompt
        system_prompt = generate_proposal_prompt(proposal)
        
        # Run AI service
        ai_result = None
        if proposal.llm.provider == "huggingface":
            ai_result = run_huggingface_model(proposal.llm.provider_model, system_prompt)
        elif proposal.llm.provider == "openai":
            pass
            # TODO
            # from llm_models.ai_services import run_openai_model
            # ai_result = run_openai_model(proposal.llm.provider_model, system_prompt)
        elif proposal.llm.provider == "gemini":
            pass
            # TODO
            # from llm_models.ai_services import run_gemini_model
            # ai_result = run_gemini_model(proposal.llm.provider_model, system_prompt)
        elif proposal.llm.provider == "anthropic":
            pass
            # TODO
            # from llm_models.ai_services import run_anthropic_model
            # ai_result = run_anthropic_model(proposal.llm.provider_model, system_prompt)
        elif proposal.llm.provider == "custom":
            # TODO
            # from llm_models.ai_services import run_custom_model
            # ai_result = run_custom_model(proposal.llm.provider_model, system_prompt)
            pass
        else:
            raise Exception(f"Unknown provider: {proposal.llm.provider}")
        
        if not ai_result:
            raise Exception("AI service returned no result")
        
        # Update proposal 
        proposal.generated_text = ai_result["text"]
        proposal.tokens_prompt = ai_result["tokens_prompt"]
        proposal.tokens_completion = ai_result["tokens_completion"]
        proposal.tokens_total = ai_result["tokens_total"]
        proposal.is_paid = True
        proposal.save()
        
        # Create billing log
        BillingLog.objects.create(
            user=proposal.user,
            proposal=proposal,
            llm=proposal.llm,
            tokens_prompt=proposal.tokens_prompt,
            tokens_completion=proposal.tokens_completion,
            cost=ai_result["cost"],
        )
        
        # Update job 
        job.result_meta = ai_result
        job.status = "completed"
        job.finished_at = timezone.now()
        job.save()
        
        # Deduct user credits
        user = proposal.user
        user.user_credits.credits -= 1
        user.user_credits.save()      

    except Exception as e:
        job.status = "failed"
        job.error = str(e)
        job.finished_at = timezone.now()
        job.save()
