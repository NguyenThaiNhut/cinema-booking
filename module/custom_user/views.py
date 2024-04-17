from datetime import datetime
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
import os
from supabase import create_client, Client, ClientOptions
import stripe

from django.contrib.auth import authenticate
from .serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer
from .models import CustomUser


# url: str = os.environ.get("SUPABASE_URL")
# key: str = os.environ.get("SUPABASE_KEY")


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


# edit profile
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


# upload image 
class ImageUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def upload_image_to_supabase(self, image):
        try:
            # Khởi tạo Supabase client
            supabase_url = settings.SUPABASE_URL
            supabase_key = settings.SUPABASE_KEY
            supabase = create_client(supabase_url, supabase_key)

            # image = file # get image from request
            bucket_name = 'Image' # bucket name is saved in supabase storage
            folder_path = 'Avatar/' # folder path in bucket is saved in supabase storage

            # response = supabase.storage.upload(bucket_name, image_name, image.file)
            # with open(image, 'rb') as f:
            #     response = supabase.storage.from_(bucket_name).upload(file=f,path="sdf", file_options={"content-type": "image/jpeg"})
            # response = supabase.storage.from_(bucket_name).upload(image.file.read(), image_name)
            current_time_integer = int(datetime.now().timestamp()) # get current time type int
            response = supabase.storage.from_(bucket_name).upload(f"{folder_path}{current_time_integer}", image.file.read(), file_options={"content-type": "image/jpeg"})
            public_url = supabase.storage.from_(bucket_name).get_public_url(f"{folder_path}{current_time_integer}")
            
            if response.status_code == 200:
                return {"err_code": 0, "message": public_url} 
            else:
                return {"err_code": 1, "message": "Avatar upload failed"}
        except Exception as e:
            return {"err_code": 2, "message": str(e)}


    def post(self, request):
        response = self.upload_image_to_supabase(request.FILES["image"])
        if response["err_code"] == 0:
            avatar = response["message"]
            user = request.user
            serializer = ProfileSerializer(user, data={"avatar": avatar}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Update avatar successful"}, status=status.HTTP_201_CREATED)
            else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else: return Response(response["message"], status=status.HTTP_400_BAD_REQUEST)

        
        
        
