from rest_framework import status, filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import CinemaBrand
from .serializers import HallSerializer, CinemaBrandSerializer


class CinemaBrandAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # get list cinema brand - all brands/brand by id
    def get(self, request, brand_id):
        try:
            if brand_id == 'ALL':
                cinema_brands = CinemaBrand.objects.all()
                serializer = CinemaBrandSerializer(cinema_brands, many=True)
                return Response(
                    {
                        "message": "Get list cinema brand successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                cinema_brand = CinemaBrand.objects.get(pk=brand_id)
                serializer = CinemaBrandSerializer(cinema_brand)
                return Response(
                    {
                        "message": "Get cinema brand successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            
        except CinemaBrand.DoesNotExist:
            return Response({"message": "Cinema brand not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # create a new cinema brand 
    def post(self, request):
        serializer = CinemaBrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                "message": "Create new cinema brand successful",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create a new hall - admin
class CreateHallAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = HallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                "message": "Create new hall successful",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
