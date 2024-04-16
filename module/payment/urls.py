from django.urls import path

from . import views
from .views import CreatePaymentSessionAPIView, HomePageView, StripeConfigAPIView, CancelledView

urlpatterns = [
    path("payment/", HomePageView.as_view(), name="payment"),
    path("payment/config/", StripeConfigAPIView.as_view(), name="payment_config"),
    
    path("payment/create-checkout-session/", CreatePaymentSessionAPIView.as_view(), name='create-checkout-session'),
    path("payment/success/", views.success_payment, name="success_payment"),
    path("payment/cancelled/", CancelledView.as_view(), name="cancelled_payment"),
    
    # path("payment/get-ro/", CreatePaymentSessionAPIView.as_view(), name='create-checkout-session'),

]
