from django.urls import path

from . import views
from .views import (
    CreatePaymentSessionAPIView, HomePageView, StripeConfigAPIView, CancelledView,
    CreateConnectAccountAPIView, CreateAccountLinkAPIView, GetConnectAccountAPIView, CreatePaymentMethodAPIView, CreatePaymentIntentInConnectAPIView, 
)

urlpatterns = [
    path("payment/", HomePageView.as_view(), name="payment"),
    path("payment/config/", StripeConfigAPIView.as_view(), name="payment_config"),
    
    path("payment/create-checkout-session/", CreatePaymentSessionAPIView.as_view(), name='create-checkout-session'),
    path("payment/success/", views.success_payment, name="success_payment"),
    path("payment/connect/success/", views.connect_success_payment, name="connect_success_payment"),
    path("payment/cancelled/", CancelledView.as_view(), name="cancelled_payment"),
    
    path("payment/create-connect-account/", CreateConnectAccountAPIView.as_view(), name="create-connect-account"),
    path("payment/create-account-link/", CreateAccountLinkAPIView.as_view(), name="create-account-link"),
    path("payment/get-connect-account/", GetConnectAccountAPIView.as_view(), name="get-connect-account"),
    path("payment/create-payment-method/", CreatePaymentMethodAPIView.as_view(), name="create-payment-method"),
    path("payment/connect/create-payment-intent/", CreatePaymentIntentInConnectAPIView.as_view(), name='create-payment-intent-in-connect'),

]
