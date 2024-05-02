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


# View for handling successful payments
def connect_success_payment(request):
    # Retrieve session ID from query parameters
    session_id = request.GET.get('session_id')
    print(request.session.get('connect_account_id'))

    if session_id:
        # Initialize Stripe API with secret key
        stripe.api_key = settings.STRIPE_SECRET_KEY
        print(request.session.get("amount"))
                            
        # connect_account_id = request.session.pop('connect_account_id', None) 
        # amount = request.session.pop('amount', None) 

        # print(connect_account_id)
        # print(amount)

        # stripe.Transfer.create(
        #     amount=amount,
        #     currency="VND",
        #     destination=connect_account_id,
        #     # application_fee=3000,
        # )  
    
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

#-------------------------------------------------
#--------------- CONNNECT STRIPE -----------------
#-------------------------------------------------

# create connect account (cgv, lotte)
class CreateConnectAccountAPIView(APIView):

    def get(self, request):
        domain_url = f"{settings.DOMAIN_NAME}/payment/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        try:
            account = stripe.Account.create(
                country="AU",
                type="express",
                capabilities={
                    "card_payments": {
                        "requested": True
                    }, 
                    "transfers": {
                        "requested": True
                    }
                },
                # business_type="individual",
                settings={
                    "payouts": {
                        "schedule": {
                            "delay_days": 3,
                            "interval": "daily"
                        },
                    }
                }
            )

            return Response(
                {
                    "message": "Create connect account successful",
                    "data": account
                }, 
                status=status.HTTP_200_OK
            )
    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_200_OK)
    

# create account link for the connect account just created
class CreateAccountLinkAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user

        domain_url = f"{settings.DOMAIN_NAME}/payment/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            if user and user.stripe_account_id:
                account_link = stripe.AccountLink.create(
                    account=user.stripe_account_id,
                    refresh_url=domain_url + "cancelled/",
                    return_url=domain_url + "cancelled/",
                    type="account_onboarding",
                )

                return Response(
                    {
                        "message": "Create account link for connect account just created successful",
                        "data": account_link
                    }, 
                    status=status.HTTP_200_OK
                )
        
            else: 
                return Response(
                    {
                        "success": False, 
                        "message": "User is not authorized to purchase"
                    }, status=status.HTTP_403_FORBIDDEN)
    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_200_OK)
        
# get info of connect account
class GetConnectAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
        
    def get(self, request):
        user = request.user

        domain_url = f"{settings.DOMAIN_NAME}/payment/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            if user and user.stripe_account_id:
                account = stripe.Account.retrieve(user.stripe_account_id)

                return Response(
                    {
                        "message": "Create account link for connect account just created successful",
                        "data": account
                    }, 
                    status=status.HTTP_200_OK
                )
        
            else: 
                return Response(
                    {
                        "success": False, 
                        "message": "User is not authorized to purchase"
                    }, status=status.HTTP_403_FORBIDDEN)
    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_200_OK)

# create payment method for customer account
class CreatePaymentMethodAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            # payment_mothod = stripe.PaymentMethod.retrieve("pm_card_visa")
            payment_method = stripe.PaymentMethod.attach(
                "pm_card_bypassPending",
                customer=user.stripe_customer_id,
            )

            return Response(
                {
                    "success": True, 
                    "payment_method": payment_method
                }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_200_OK)

# create payment intent
class CreatePaymentIntentInConnectAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            if user and user.stripe_customer_id:
                customer_id = user.stripe_customer_id
                pm_id = user.stripe_pm_id
                connect_account_id = request.data["connect_account_id"]

                amount = 3.95  
                amount_aud  = int(amount*100)

                application_fee_amount = amount * 0.05
                application_fee_amount_aud = int(application_fee_amount*100)

                # create payment intent from customer to stripe
                payment_intent = stripe.PaymentIntent.create(
                    amount=amount_aud,
                    currency='AUD',
                    customer=customer_id,
                    payment_method_types=["card"],
                    payment_method = pm_id,
                    confirm=True,
                )

                charge_id = payment_intent.latest_charge
       
                # Check status of PaymentIntent after confirmed
                if payment_intent.status == 'succeeded':
                    print('Payment success!')

                    # create tranfer from payment intent just created to connect account 
                    # collected fees for the platform (application_fee_amount_aud)
                    transfer = stripe.Transfer.create(
                        amount=amount_aud-application_fee_amount_aud,
                        currency="AUD",
                        source_transaction=charge_id,
                        destination=connect_account_id,
                    )
                else: print('Payment failed:', payment_intent.status)

                return Response(
                    {
                        "success": True, 
                        "payment_intent": payment_intent,
                        "transfer": transfer
                        # "sessionId": checkout_session["id"],
                        # "url": checkout_session["url"]
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
    stripe.api_key = settings.STRIPE_SECRET_KEY

    balance = stripe.Balance.retrieve()
    available_balance = balance['available'][0]['amount']
    
    if available_balance > 0:
        stripe.Payout.create(
            amount=available_balance,
            currency="AUD",
        )

# Set up recurring payments on Friday every 2 weeks
start_scheduler_payment(pay_out_to_my_bank)
