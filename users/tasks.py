from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from celery import shared_task
from celery.exceptions import Retry
import logging
# import local 
from users.models import User

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_verification_email(self, user_id):
    try:
        print(" *************** Debug send verification email *************** ")
        user = User.objects.get(pk=user_id)
        
        # Generate uid and token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Build verification link
        verification_link = f"{getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')}/verify-email/{uid}/{token}/"
        
        # Render the HTML template with context
        message = render_to_string(
            "users/verification_mail.html",
            {
                "user": user,
                "verification_link": verification_link,
            },
        )

        # Send the email
        send_mail(
            subject="Verify your email",
            message="",
            html_message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        logger.info(f"Verification email sent successfully to user {user_id}")
        
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found")
        return
    except Exception as e:
        logger.error(f"Failed to send verification email to user {user_id}: {e}")
        raise self.retry(exc=e)