from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers

# Create your views here.


class CreateSubsctiptionWithStripeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = serializers.StripeSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan_id = serializer.validated_data["plan_id"]
        selected_plan = models.Plan.objects.get(id=plan_id)
        
        # Create a subscription record
        subscription = models.Subsctiption.objects.create(
            user=request.user,
            plan=selected_plan,
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
        
        
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
