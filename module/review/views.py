from rest_framework import status, filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail

from .models import ReviewTag, Review 

from .serializers import (
    ReviewTagSerializer, ReviewSerializer,
)


# api of admins
# CRUD review tag
# get review tag
class GetListReviewTagAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # get list review tag - all tags/tag by id
    def get(self, request, tag_id):
        try:
            if tag_id == 'ALL':
                review_tags = ReviewTag.objects.all()
                serializer = ReviewTagSerializer(review_tags, many=True)
                return Response(
                    {
                        "message": "Get list review tag successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                review_tag = ReviewTag.objects.get(pk=tag_id)
                serializer = ReviewTagSerializer(review_tag)
                return Response(
                    {
                        "message": "Get review tag successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            
        except ReviewTag.DoesNotExist:
            return Response({"message": "Review tag not found"}, status=status.HTTP_404_NOT_FOUND)
        
# create/update/delete review tag
class ReviewTagAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    # create a new review tag 
    def post(self, request):
        serializer = ReviewTagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                "message": "Create new review tag successful",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # update an existing review tag
    def put(self, request, tag_id):
        try:
            tag = ReviewTag.objects.get(pk=tag_id)
            serializer = ReviewTagSerializer(tag, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Update review tag successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except ReviewTag.DoesNotExist:
            return Response({"message": "Review tag not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # delete an existing review tag
    def delete(self, request, tag_id):
        try:
            tag = ReviewTag.objects.get(pk=tag_id)
            tag.delete()
            return Response({"message": "Delete review tag successfully"}, status=status.HTTP_204_NO_CONTENT)
    
        except ReviewTag.DoesNotExist:
            return Response({"message": "Review tag not found"}, status=status.HTTP_404_NOT_FOUND)
        
# get movie's reviews 
class GetMovieReviewsAPIView(APIView):
    def get(self, request, movie_id):
        try:
            reviews = Review.objects.filter(movie_id=movie_id)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(
                {
                    "message": "Get list of reviews for the movie successful",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Review.DoesNotExist:
            return Response({"message": "Reviews for the movie not found"}, status=status.HTTP_404_NOT_FOUND)


class ReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # create a new review  
    def post(self, request):
        user = request.user
        request.data["customer"] = user.id
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                "message": "Create new review successful",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update a review 
    def put(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({"message": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user 
        if review.customer.id != user.id:
            return Response({"message": "You do not have permission to update this review"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


