from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import ScreeningPrice, Screening
from .serializers import ScreeningPriceSerializer, ScreeningSerializer

# CRUD screening price
# get screening price
class GetListScreeningPriceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # get list screening price - all screening prices/screening price by id
    def get(self, request, price_id):
        try:
            if price_id == 'ALL':
                prices = ScreeningPrice.objects.all().order_by('id')
                serializer = ScreeningPriceSerializer(prices, many=True)
                return Response(
                    {
                        "message": "Get list screening price successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                price = ScreeningPrice.objects.get(pk=price_id)
                serializer = ScreeningPriceSerializer(price)
                return Response(
                    {
                        "message": "Get screening price successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            
        except ScreeningPrice.DoesNotExist:
            return Response({"message": "Screening price not found"}, status=status.HTTP_404_NOT_FOUND)

# create/update/delete screening price
class ScreeningPriceAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    # create a new screening price
    def post(self, request):
        serializer = ScreeningPriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Create new screening price successful",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update an existing screening price
    def put(self, request, price_id):
        try:
            price = ScreeningPrice.objects.get(pk=price_id)
            serializer = ScreeningPriceSerializer(price, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Update screening price successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except ScreeningPrice.DoesNotExist:
            return Response({"message": "Screening price not found"}, status=status.HTTP_404_NOT_FOUND)

    # delete an existing screening price
    def delete(self, request, price_id):
        try:
            price = ScreeningPrice.objects.get(pk=price_id)
            price.delete()
            return Response({"message": "Delete screening price successfully"}, status=status.HTTP_204_NO_CONTENT)
    
        except ScreeningPrice.DoesNotExist:
            return Response({"message": "Screening price not found"}, status=status.HTTP_404_NOT_FOUND)
        

# CRUD screening
# get screening
class GetListScreeningAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # get list screening - all screenings/screening by id
    def get(self, request, screening_id):
        try:
            if screening_id == 'ALL':
                screenings = Screening.objects.all().order_by('id')
                serializer = ScreeningSerializer(screenings, many=True)
                return Response(
                    {
                        "message": "Get list screening successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                screening = Screening.objects.get(pk=screening_id)
                serializer = ScreeningSerializer(screening)
                return Response(
                    {
                        "message": "Get screening successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
        except Screening.DoesNotExist:
            return Response({"message": "Screening not found"}, status=status.HTTP_404_NOT_FOUND)

# create/update/delete screening
class ScreeningAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    # create a new screening
    def post(self, request):
        serializer = ScreeningSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Create new screening successful",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # update an existing screening
    def put(self, request, screening_id):
        try:
            screening = Screening.objects.get(pk=screening_id)
            serializer = ScreeningSerializer(screening, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Update screening successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Screening.DoesNotExist:
            return Response({"message": "Screening not found"}, status=status.HTTP_404_NOT_FOUND)

    # delete an existing screening
    def delete(self, request, screening_id):
        try:
            screening = Screening.objects.get(pk=screening_id)
            screening.delete()
            return Response({"message": "Delete screening successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Screening.DoesNotExist:
            return Response({"message": "Screening not found"}, status=status.HTTP_404_NOT_FOUND)



