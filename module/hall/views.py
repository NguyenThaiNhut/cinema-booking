from rest_framework import status, filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import send_mail

from .models import Address, CinemaBrand, Cinema, HallType, Hall, SeatType, SeatDetail
from module.screening.models import Screening
from module.custom_user.models import CustomUser, UserFavoriteCinema

from .serializers import (
    CinemaBrandSerializer, CinemaSerializer, 
    HallTypeSerializer, HallSerializer, 
    SeatTypeSerializer, SeatSerializer,
    AddressSerializer, 
    UserFavoriteCinemaSerializer,
)
from module.screening.serializers import ScreeningSerializer
from module.custom_user.serializers import ProfileSerializer

# api of admins
# CRUD cinema brand
# get cinema brand
class GetListCinemaBrandAPIView(APIView):
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
        
# create/update/delete cinema brand
class CinemaBrandAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
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
    
    # update an existing cinema brand
    def put(self, request, brand_id):
        try:
            brand = CinemaBrand.objects.get(pk=brand_id)
            serializer = CinemaBrandSerializer(brand, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Update cinema brand successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except CinemaBrand.DoesNotExist:
            return Response({"message": "Cinema brand not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # delete an existing cinema brand
    def delete(self, request, brand_id):
        try:
            brand = CinemaBrand.objects.get(pk=brand_id)
            brand.delete()
            return Response({"message": "Delete cinema brand successfully"}, status=status.HTTP_204_NO_CONTENT)
    
        except CinemaBrand.DoesNotExist:
            return Response({"message": "Cinema brand not found"}, status=status.HTTP_404_NOT_FOUND)


# CRUD cinema
# get cinema
class GetListCinemaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # get list cinema - all brands/brand by id
    def get(self, request, cinema_id):
        try:
            if cinema_id == 'ALL':
                cinemas = Cinema.objects.all()
                serializer = CinemaSerializer(cinemas, many=True)
                return Response(
                    {
                        "message": "Get list cinema successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                cinema_brand = Cinema.objects.get(pk=cinema_id)
                serializer = CinemaSerializer(cinema_brand)
                return Response(
                    {
                        "message": "Get cinema successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            
        except Cinema.DoesNotExist:
            return Response({"message": "Cinema not found"}, status=status.HTTP_404_NOT_FOUND)

# create/update/delete cinema
class CinemaAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    # create a new cinema 
    def post(self, request):
        serializer = CinemaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                "message": "Create new cinema successful",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # update an existing cinema
    def put(self, request, cinema_id):
        try:
            cinema = Cinema.objects.get(pk=cinema_id)
            serializer = CinemaSerializer(cinema, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Update cinema successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Cinema.DoesNotExist:
            return Response({"message": "Cinema not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # delete an existing cinema
    def delete(self, request, cinema_id):
        try:
            cinema = Cinema.objects.get(pk=cinema_id)
            cinema.delete()
            return Response({"message": "Delete cinema successfully"}, status=status.HTTP_204_NO_CONTENT)
    
        except Cinema.DoesNotExist:
            return Response({"message": "Cinema not found"}, status=status.HTTP_404_NOT_FOUND)


# CRUD hall type
# get hall type
class GetListHallTypeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # get list hall type - all hall types/hall type by id
    def get(self, request, type_id):
        try:
            if type_id == 'ALL':
                types = HallType.objects.all().order_by('id')
                serializer = HallTypeSerializer(types, many=True)
                return Response(
                    {
                        "message": "Get list hall type successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                type = HallType.objects.get(pk=type_id)
                serializer = HallTypeSerializer(type)
                return Response(
                    {
                        "message": "Get hall type successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            
        except HallType.DoesNotExist:
            return Response({"message": "Hall type not found"}, status=status.HTTP_404_NOT_FOUND)

# create/update/delete hall type
class HallTypeAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    # create a new hall type 
    def post(self, request):
        serializer = HallTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                "message": "Create new hall type successful",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # update an existing hall type
    def put(self, request, type_id):
        try:
            type = HallType.objects.get(pk=type_id)
            serializer = HallTypeSerializer(type, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Update hall type successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except HallType.DoesNotExist:
            return Response({"message": "Hall type not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # delete an existing hall type
    def delete(self, request, type_id):
        try:
            type = HallType.objects.get(pk=type_id)
            type.delete()
            return Response({"message": "Delete hall type successfully"}, status=status.HTTP_204_NO_CONTENT)
    
        except HallType.DoesNotExist:
            return Response({"message": "Hall type not found"}, status=status.HTTP_404_NOT_FOUND)


# CRUD hall
# get hall
class GetListHallAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # get list hall - all halls/hall by id
    def get(self, request, hall_id):
        try:
            if hall_id == 'ALL':
                halls = Hall.objects.all().order_by('id')
                serializer = HallSerializer(halls, many=True)
                return Response(
                    {
                        "message": "Get list hall successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                hall = Hall.objects.get(pk=hall_id)
                serializer = HallSerializer(hall)
                return Response(
                    {
                        "message": "Get hall successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            
        except Hall.DoesNotExist:
            return Response({"message": "Hall not found"}, status=status.HTTP_404_NOT_FOUND)

# create/update/delete hall
class HallAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    # create a new hall 
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
    
    # update an existing hall
    def put(self, request, hall_id):
        try:
            hall = Hall.objects.get(pk=hall_id)
            serializer = HallSerializer(hall, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Update hall successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Hall.DoesNotExist:
            return Response({"message": "Hall not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # delete an existing hall
    def delete(self, request, hall_id):
        try:
            type = Hall.objects.get(pk=hall_id)
            type.delete()
            return Response({"message": "Delete hall successfully"}, status=status.HTTP_204_NO_CONTENT)
    
        except Hall.DoesNotExist:
            return Response({"message": "Hall not found"}, status=status.HTTP_404_NOT_FOUND)


# CRUD seat type
# get seat type
class GetListSeatTypeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # get list seat type - all seat types/seat type by id
    def get(self, request, type_id):
        try:
            if type_id == 'ALL':
                types = SeatType.objects.all().order_by('id')
                serializer = SeatTypeSerializer(types, many=True)
                return Response(
                    {
                        "message": "Get list seat type successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                type = SeatType.objects.get(pk=type_id)
                serializer = SeatTypeSerializer(type)
                return Response(
                    {
                        "message": "Get seat type successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            
        except SeatType.DoesNotExist:
            return Response({"message": "seat type not found"}, status=status.HTTP_404_NOT_FOUND)

# create/update/delete seat type
class SeatTypeAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    # create a new seat type 
    def post(self, request):
        serializer = SeatTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                "message": "Create new seat type successful",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # update an existing seat type
    def put(self, request, type_id):
        try:
            type = SeatType.objects.get(pk=type_id)
            serializer = SeatTypeSerializer(type, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Update seat type successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except SeatType.DoesNotExist:
            return Response({"message": "Seat type not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # delete an existing seat type
    def delete(self, request, type_id):
        try:
            type = SeatType.objects.get(pk=type_id)
            type.delete()
            return Response({"message": "Delete seat type successfully"}, status=status.HTTP_204_NO_CONTENT)
    
        except SeatType.DoesNotExist:
            return Response({"message": "Seat type not found"}, status=status.HTTP_404_NOT_FOUND)


# CRUD seat
# get seat
class GetListSeatAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # get list seat - all seat types/seat by id
    def get(self, request, seat_id):
        try:
            if seat_id == 'ALL':
                seats = SeatDetail.objects.all().order_by('id')
                serializer = SeatSerializer(seats, many=True)
                return Response(
                    {
                        "message": "Get list seat successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                seat = SeatDetail.objects.get(pk=seat_id)
                serializer = SeatSerializer(seat)
                return Response(
                    {
                        "message": "Get seat successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            
        except SeatDetail.DoesNotExist:
            return Response({"message": "Seat not found"}, status=status.HTTP_404_NOT_FOUND)

# create/update/delete seat
class SeatAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    
    # create a new seat 
    def post(self, request):
        serializer = SeatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                "message": "Create new seat successful",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # update an existing seat type
    def put(self, request, seat_id):
        try:
            seat = SeatDetail.objects.get(pk=seat_id)
            serializer = SeatSerializer(seat, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Update seat successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except SeatDetail.DoesNotExist:
            return Response({"message": "Seat not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # delete an existing seat type
    def delete(self, request, seat_id):
        try:
            seat = SeatDetail.objects.get(pk=seat_id)
            seat.delete()
            return Response({"message": "Delete seat successfully"}, status=status.HTTP_204_NO_CONTENT)
    
        except SeatDetail.DoesNotExist:
            return Response({"message": "Seat not found"}, status=status.HTTP_404_NOT_FOUND)


# api of customers
# get list address (province)
class GetListAddressAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    # get list address
    def get(self, request):
        try:
            addresses = Address.objects.all()
            serializer = AddressSerializer(addresses, many=True)
            return Response(
                {
                    "message": "Get list addresses successful",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
            
        except Address.DoesNotExist:
            return Response({"message": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        
#search list address by province
class SearchAddressAPIView(generics.ListAPIView): # "search=" is default key
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["province"]

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "message": "Get list addresses successful",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    

# get list cinemas (by province)
class GetListCienmaAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    # get list cinema by address_id
    def get(self, request, address_id):
        try:
            addresses = Address.objects.get(pk=address_id)
            cinemas = Cinema.objects.filter(address=addresses)
            serializer = CinemaSerializer(cinemas, many=True)
            return Response(
                {
                    "message": "Get list cinemas successful",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
            
        except Address.DoesNotExist:
            return Response({"message": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        
# search cinema by name (province)
class SearchCinemaAPIView(generics.ListAPIView): # "search=" is default key
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]

    def list(self, request):
        address_id = request.query_params.get("address_id")
        if address_id:
            try:
                queryset = self.filter_queryset(self.get_queryset().filter(address_id=address_id))
            except Address.DoesNotExist:
                return Response({"message": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "message": "Get list cinemas successful",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    
# filter cinema by cinema brand
class FilterCinemaByBrandAPIView(generics.ListAPIView):
    queryset = Cinema.objects.all()
    serializer_class = CinemaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"brand"}

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        address_id = self.request.query_params.get("address_id")

        if address_id:
            queryset = Cinema.objects.filter(address_id=address_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "message": "Get list cinemas successful",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        return super().get(request, *args, **kwargs)
    
# get details cinema
class GetDetailCienmaAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    # get detail cinema by address_id
    def get(self, request, cinema_id):
        screenings = Screening.objects.filter(hall__cinema__id=cinema_id).order_by("-start_time")
        serializer = ScreeningSerializer(screenings, many=True)
        # serializer_cinema = CinemaSerializer(cinema)
        return Response(
            {
                "message": "Get detail cinema successful",
                "data": serializer.data
            },
            status=status.HTTP_200_OK,
        )
            
        
# add cinema to user's favorites cinema
class UserFavoriteCinemaAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    # get list cinemas from user's favorites cinema
    def get(self, request):
        user_id = request.user.id
        cinemas = UserFavoriteCinema.objects.filter(user_id=user_id)
        serializer = UserFavoriteCinemaSerializer(cinemas, many=True)
        return Response(
            {
                "message": "Get list cinemas from user's favorite cinema successful",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
        
    # add cinema to user's favorite cinemas 
    def post(self, request):
        user_id = request.user.id 
        cinema_id = request.data.get('cinema_id') 
        
        if UserFavoriteCinema.objects.filter(user_id=user_id, cinema_id=cinema_id).exists():
            return Response({"message": "This cinema is already in your favorite list"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserFavoriteCinemaSerializer(data={"user_id": user_id, "cinema_id": cinema_id})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Added cinema to favorite list successfully", 
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # delete cinema to user's favorite cinemas 
    def delete(self, request, user_favorite_cinema_id):
        try:
            user_favorite_cinema = UserFavoriteCinema.objects.get(pk=user_favorite_cinema_id)
            user_favorite_cinema.delete()
            return Response({"message": "Delete cinema from the user's favorite cinema successfully"}, status=status.HTTP_204_NO_CONTENT)
    
        except UserFavoriteCinema.DoesNotExist:    
            return Response({"message": "Cinema not found"}, status=status.HTTP_404_NOT_FOUND)

class SendEmailAPIView(APIView):
    def post(self, request):
        sender_email = request.data.get('sender_email', 'nguyenthainhut005@gmail.com')
        recipient_email = request.data.get('recipient_email', 'nguyenthainhut001@gmail.com')

        try:
            send_mail(
                "Subject here",
                "Here is the message.",
                sender_email,
                [recipient_email],
                fail_silently=False,
            )
            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Failed to send email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








