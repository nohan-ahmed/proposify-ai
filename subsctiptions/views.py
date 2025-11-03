from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import transaction
# import rest framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# import third-party libraries
import stripe
from django.conf import settings
# import local modules
from . import models
from . import serializers

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateSubsctiptionWithStripeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = serializers.StripeSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan_id = serializer.validated_data["plan_id"]
        selected_plan = models.Plan.objects.get(id=plan_id)
        
        with transaction.atomic():
            # Check if the user already has a subscription
            # existing_subscription = models.Subsctiption.objects.filter(
            #     user=request.user, status="confirmed"
            # ).first()
            # if existing_subscription:
            #     return Response(
            #         {"error": "You already have an active subscription."},
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )
            
            # Create a subscription record
            subscription = models.Subsctiption.objects.create(
                user=request.user,
                plan=selected_plan,
                status="pending",
                total_amount=selected_plan.discount_price,
            )

            # Create a payment record for the subscription
            payment = models.Payment.objects.create(
                subscription=subscription,
                user=request.user,
                method="stripe",
                status="pending",
                paid_at=None # Set this to the actual payment date
            )

        # create a stripe checkout session
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": f"{selected_plan.name} Plan",
                            },
                            "unit_amount": int(
                                selected_plan.discount_price * 100
                            ),  # Amount (in cents)
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                metadata={"subscription_id": subscription.id},
                success_url=f"http://127.0.0.1:5500//success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"http://127.0.0.1:5500/cancel",
            )
            # Return the session ID and the checkout URL to the client
            return Response({"id": checkout_session.id, "url": checkout_session.url})
        except Exception as e:
            return Response({"error": str(e)}, status=400)


endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.headers.get('stripe-signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle checkout session completed
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Get order ID from metadata
        subscription_id = session.get('metadata', {}).get('subscription_id')
        payment_intent_id = session.get('payment_intent')
        
        if subscription_id and payment_intent_id:
            try:
                payment = models.Payment.objects.get(
                    subscription_id=subscription_id,
                    method='stripe',
                    status='pending'
                )
                
                # Update payment status
                payment.status = 'success'
                payment.transaction_id = payment_intent_id
                payment.paid_at = timezone.now()
                payment.save()
                
                # Update subscription status
                payment.subscription.status = 'confirmed'
                payment.subscription.save()
                
                # 
                user = payment.user
                user.user_credits.credits = user.user_credits.credits + payment.subscription.plan.credits
                user.user_credits.save()
                
                
            except models.Payment.DoesNotExist:
                pass
    
    return HttpResponse(status=200)
