from rest_framework import status, filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Count
from datetime import date

from .models import Movie
from .serializers import MovieSerializer

from module.booking.models import Booking
from module.booking.serializers import BookingSerializer
from module.utils import ImageUploader


# get list of movies
class ListMovieAPIView(APIView):
    # permission_classes = [IsAdminUser]
    # authentication_classes = [JWTAuthentication]

    def get(self, request, movie_id):
        try:
            if movie_id == 'ALL':
                movies = Movie.objects.all()
                serializer = MovieSerializer(movies, many=True)
                return Response(
                    {
                        "message": "Get list movie successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                movie = Movie.objects.get(pk=movie_id)
                serializer = MovieSerializer(movie)
                return Response(
                    {
                        "message": "Get movie successful",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            
        except Movie.DoesNotExist:
            return Response({"message": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

# CUD movie
class MovieAPIView(APIView):
    # permission_classes = [IsAdminUser]
    # authentication_classes = [JWTAuthentication]

    # create a new movie
    def post(self, request):
        print(request.data)
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                "message": "Create new movie successful",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # update a movie by its id
    def put(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
            serializer = MovieSerializer(movie, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(
                {
                    "message": "Update movie successful",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Movie.DoesNotExist:
            return Response({"message": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # delete a movie by its id
    def delete(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"message": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        
        movie.delete()
        return Response({"message": "Delete movie successfully"}, status=status.HTTP_204_NO_CONTENT)
    
# upload movie poster
class PosterUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def put(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            return Response({"message": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        
        bucket_name = "Movie" # bucket name
        response = ImageUploader.upload_image_to_supabase(request.FILES["image"], bucket_name)
        if response["err_code"] == 0:
            poster = response["image_url"]
            poster_name = response["image_name"]

            if movie.poster and movie.poster_name:
            # if the user has a previous avatar, delete the old avatar
                ImageUploader.delete_old_image(bucket_name, movie.poster_name)

            serializer = MovieSerializer(movie, data={"poster": poster, "poster_name": poster_name}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Update movie poster successful"}, status=status.HTTP_201_CREATED)
            else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else: return Response(response["message"], status=status.HTTP_400_BAD_REQUEST)


# class CustomSearchFilter(filters.SearchFilter):
#     def get_search_fields(self, view, request):
#         if request.query_params.get('director_and_actor_only'):
#             return ['director_and_actor__description']
#         return super().get_search_fields(view, request)
    
#search list movie by title and language name
class SearchMovieAPIView(generics.ListAPIView): # "search=" is default key
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "language__name"]
    
# filter list movies by language name
class FilterMovieAPIView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {"language"}


# class FilterMovieAPIView(generics.ListAPIView):
#     serializer_class = MovieSerializer

#     def get_queryset(self):
#         """
#         Optionally restricts the returned purchases to a given user,
#         by filtering against a `username` query parameter in the URL.
#         """
#         queryset = Movie.objects.all()
#         title = self.request.query_params.get('title')
#         print(title)
#         if title is not None:
#             queryset = queryset.filter(title=title)
#         return queryset


# get list of current showing movies 
class GetListCurrentShowingMovieAPIView(APIView):

    def get(self, request):
        current_date = date.today()
        movies = Movie.objects.filter(release_date__lt=current_date)
        serializer = MovieSerializer(movies, many=True)
        return Response(
            {
                "message": "Get list of current showing movies successful",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    

# get list of upcoming movies 
class GetListUpcomingMovieAPIView(APIView):

    def get(self, request):
        current_date = date.today()
        movies = Movie.objects.filter(release_date__gt=current_date)
        serializer = MovieSerializer(movies, many=True)
        return Response(
            {
                "message": "Get list of upcoming movies successful",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    

# get list of featured movies
class GetListFeatureMovieAPIView(APIView):
    
    def get(self, request):
        top_movies = Booking.objects.values('screening__movie__id').annotate(num_bookings=Count('id')).order_by('-num_bookings')[:3]
        top_movie_ids = [movie['screening__movie__id'] for movie in top_movies]
        movies = Movie.objects.filter(id__in=top_movie_ids)

        print(top_movie_ids)
        movies = sorted(movies, key=lambda x: top_movie_ids.index(x.id))

        for movie in movies:
            for top_movie in top_movies:
                if top_movie['screening__movie__id'] == movie.id:
                    movie.num_bookings = top_movie['num_bookings']
                    break

        serializer = MovieSerializer(movies, many=True)
        return Response(
            {
                "message": "Get list of upcoming movies successful",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    
# get details of a movie
class DetailMovieAPIView(APIView):

    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
            serializer = MovieSerializer(movie)
            return Response(
                {
                    "message": "Get details of a movie successful",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Movie.DoesNotExist:
            return Response({"message": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
