from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import BookSerializer, ReviewSerializer, UserSerializer
from base.models import Book, Review, User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.username
        # ...
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
        '/api/book/',
        '/api/review/<int:book_id>',
        '/api/userHome/<str:name>',
    ]
    return Response(routes)



@api_view(['GET'])
def getBooks(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getReview(request, book_id):
    reviews = Review.objects.filter(book=book_id)
    # many kw just wants to know if it's a query set or not, it can be a set of one or no results... 
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userHome(request, name):
    if request.user.username != name:
        return Response(data=None, status=status.HTTP_401_UNAUTHORIZED)
    serializer = ReviewSerializer(request.user.reviews, many=True)
    return Response(serializer.data)