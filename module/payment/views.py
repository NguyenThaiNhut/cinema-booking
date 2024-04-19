from django.conf import settings  # new
from django.http.response import JsonResponse  # new
from django.views.decorators.csrf import csrf_exempt  # new
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework import status, filters, generics
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.template import loader

from django.views.generic.base import TemplateView
import stripe
import json

import schedule
import time
import datetime

from module.schedulers import start_scheduler_payment


# from module.screening.models import Screening
# from module.seat_detail.models import SeatDetail
# from module.booking.models import Booking


# View for the home page
class HomePageView(TemplateView):
    template_name = "payment/payment.html"

# View for handling successful payments
def success_payment(request):
    # Retrieve session ID from query parameters
    session_id = request.GET.get('session_id')

    if session_id:
        # Initialize Stripe API with secret key
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Retrieve checkout session using session ID
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        print(checkout_session)

        # List payment methods associated with the customer
        list_payment_methods_of_cus = stripe.Customer.list_payment_methods(checkout_session.customer)
        print(list_payment_methods_of_cus)
    
    # Render success template
    template = loader.get_template("payment/success.html")
    context = {}
    return HttpResponse(template.render(context, request))

# View for handling cancelled payments
class CancelledView(TemplateView):
    template_name = "payment/cancelled.html"

# API view for retrieving Stripe configuration
class StripeConfigAPIView(APIView):
    def get(self, request):
        # Construct Stripe configuration object with public key
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return Response(stripe_config)


# API view for creating a payment session
class CreatePaymentSessionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user

        domain_url = f"{settings.DOMAIN_NAME}/payment/"
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            if user and user.stripe_customer_id:
                customer_id = user.stripe_customer_id

                # stripe.PaymentMethod.create(
                #     type="card",
                #     card={
                #         "number": "4242424242424242",
                #         "exp_month": 8,
                #         "exp_year": 2026,
                #         "cvc": "314",
                #     },
                # )

                checkout_session = stripe.checkout.Session.create(
                    customer=customer_id,
                    success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
                    cancel_url=domain_url + "cancelled/",
                    payment_method_types=["card"],
                    # setup_future_usage=off_session
                    mode="payment",
                    # phone_number_collection={"enabled": True},
                    line_items=[
                        {
                            "price_data": {
                                "currency": "vnd",
                                "unit_amount": 100000,
                                "product_data": {
                                    "name": "Ticket",
                                    "description": "Ticket",
                                    "images": [
                                        "https://qjjqzsggbnviynblzjgz.supabase.co/storage/v1/object/public/Image/Avatar/1711966129?"
                                    ],
                                },
                            },
                            "quantity": 1,
                        }
                    ],
                )

                print(checkout_session["url"])
                return Response(
                    {
                        "success": True, 
                        "sessionId": checkout_session["id"]
                    }, status=status.HTTP_200_OK)
            else: 
                return Response(
                    {
                        "success": False, 
                        "message": "User is not authorized to purchase"
                    }, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_200_OK)


# Background task for processing payouts to bank account
def pay_out_to_my_bank():
    print("Running job at", datetime.datetime.now())
    stripe.api_key = settings.STRIPE_SECRET_KEY

    balance = stripe.Balance.retrieve()
    print(balance)
    available_balance = balance['available'][0]['amount']
    
    if available_balance > 0:
        stripe.Payout.create(
            amount=available_balance,
            currency="AUD",
        )

# Set up recurring payments on Friday every 2 weeks
start_scheduler_payment(pay_out_to_my_bank)
