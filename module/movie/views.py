from rest_framework import status, filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie
from .serializers import MovieSerializer

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
    filterset_fields = {"language__name"}


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
