from datetime import datetime
from django.utils import timezone
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

import os
from supabase import create_client, Client, ClientOptions
import stripe
import random
from threading import Thread
import time
from random import randint
from django.core.mail import send_mail

from django.contrib.auth import authenticate
from .serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer
from .models import CustomUser, VerificationCode
from module.schedulers import start_scheduler_custom_user
from module.utils import ImageUploader


# register
class RegistrationAPIView(APIView):
    def post(self, request):
        data = request.data

        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY

            # create new customer in stripe
            customer = stripe.Customer.create(
                email = data["email"], 
                name = data["username"], 
                phone = data["phone_number"],
            )

            serializer.save(stripe_customer_id=customer.id)
            return Response(
                {
                    "message": "Register successful", 
                    "user": serializer.data
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # creat token
            refresh = RefreshToken.for_user(user)

            payload = refresh.payload
            payload['email'] = user.email
            refresh.payload = payload

            access = str(refresh.access_token)
            return Response(
                {
                    "message": "Login successful",
                    "user_id": user.id,
                    "access_token": access,
                    "refresh_token": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# logout
class LogoutAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Error logging out"}, status=status.HTTP_400_BAD_REQUEST)
        
    
# refresh token 
class RefreshTokenAPIView(APIView):
    def post(self, request):

        print(request)
        refresh_token = request.data['access_token']

        print(refresh_token)

        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# get profile
class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        # return Response(
        #     {
        #         "message": "Get profile successful",
        #         "user": serializer.data,
        #     },
        #     status=status.HTTP_200_OK,
        # )
        return Response(serializer.data, status=status.HTTP_200_OK)


# update profile
class EditProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request):
        user = request.user

        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                "message": "Update profile successful",
                "user": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# upload avatar user
class ImageUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request):
        # response = self.upload_image_to_supabase(request.FILES["image"])
        bucket_name = "Avatar" # bucket name
        response = ImageUploader.upload_image_to_supabase(request.FILES["image"], bucket_name)
        if response["err_code"] == 0:
            avatar = response["image_url"]
            avatar_name = response["image_name"]

            user = request.user
            if user.avatar and user.avatar_name:
            # if the user has a previous avatar, delete the old avatar
                ImageUploader.delete_old_image(bucket_name, user.avatar_name)

            serializer = ProfileSerializer(user, data={"avatar": avatar, "avatar_name": avatar_name}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Update avatar successful"}, status=status.HTTP_201_CREATED)
            else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else: return Response(response["message"], status=status.HTTP_400_BAD_REQUEST)


# code validation
class CodeValidationAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def random_with_N_digits(self, n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)
    
    # create a new code validation and send code validation to email of the user
    def get(self, request):
        user = request.user
        random_number = self.random_with_N_digits(6)

        try:
            # update or create a verification code for an user
            verification_code, created = VerificationCode.objects.update_or_create(
                user=user,
                defaults={
                    'code': random_number,
                    'created_at': timezone.now(),
                    'expires_at': timezone.now() + timezone.timedelta(seconds=60)
                }
            )

            if user and user.email:
                sender_email = settings.EMAIL_HOST_USER
                recipient_email = user.email

                try:
                    send_mail(
                        "Code",
                        f"{random_number}",
                        sender_email,
                        [recipient_email],
                        fail_silently=False,
                    )
                except Exception as e:
                    return Response({"message": "Failed to send email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                "message": "Verification code created successfully",
                "code": random_number,
                "created": created
            }, 
            status=status.HTTP_201_CREATED)
        
        except Exception as e:
            # Xử lý nếu có lỗi xảy ra
            return Response({"message": "Failed to create verification code", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    # check verification code
    def post(self, request):
        user = request.user
        code = request.data.get('code')

        try:
            verification_code = VerificationCode.objects.get(user=user, code=code)

            current_time = timezone.now()
            if current_time < verification_code.expires_at:
                return Response({"message": "Verification code is valid"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Authentication code expired"}, status=status.HTTP_400_BAD_REQUEST)

        except VerificationCode.DoesNotExist:
            return Response({"message": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)

# update password 
class PasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request):
        username = request.user.username
        new_password = request.data.get('new_password')

        try:
            user = CustomUser.objects.get(username=username)

            user.set_password(new_password)
            user.save()

            return Response({"message": "Password updated successful"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            
# Set up remove expired refresh tokens in blacklist function
def remove_expired_refresh_tokens():
    current_time_utc = datetime.now(timezone.utc)
    OutstandingToken.objects.filter(expires_at__lt=current_time_utc).delete()

start_scheduler_custom_user(remove_expired_refresh_tokens)

        
        
        
