from django.core.checks.messages import Error
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import BookSerializer, ReviewSerializer, UserSerializer
from base.models import Book, Review, User
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

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

@api_view(['POST'])
def register(request):
    try:
        new_user = User.objects.create_user(username=request.data['username'], password=request.data['password'])
        context = {"message": "User successfully created.", "username": new_user.username}
        return Response(data=context, status=status.HTTP_201_CREATED)
    except IntegrityError:
        taken_name = request.data['username']
        context = {"message": f"Username {taken_name} already taken."}
        return Response(data=context, status=status.HTTP_409_CONFLICT)  
        
        

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
    # We can also serialize querysets instead of model instances. To do so we simply add a many=True flag to the serializer arguments.
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

# ~~~Reviews ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# get all reviews for single book
@api_view(['GET'])
def review_list(request, book_id):
    # GET
    if request.method == 'GET':
        reviews = Review.objects.filter(book=book_id)
        # many kw just wants to know if it's a query set or not, it can be a set of one or no results... 
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

# CRUD for a user's review  
@api_view(['PUT', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def review(request, book_id):
    print("req data:::   ", request.data)
    #POST 
    if request.method == 'POST':
        serial = ReviewSerializer(data=request.data)
        if serial.is_valid():
            try:
                serial.save(user=request.user)
                return Response(serial.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(data={"message": "You have already reviewed this title. You may update your review, or delete it and make a new one."} ,status=status.HTTP_409_CONFLICT)
    try:
        review = Review.objects.get(book=book_id, user=request.user.id)
        serial = ReviewSerializer(review, many=False)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
 
    # PUT
    if request.method == 'PUT':
        serial = ReviewSerializer(review, data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=status.HTTP_200_OK)
        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # DELETE
    elif request.method == 'DELETE':
        review.delete()
        return Response("Review succesfully deleted", status=status.HTTP_204_NO_CONTENT)

# ~~~R ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userHome(request, name):
    if request.user.username != name:
        return Response(data=None, status=status.HTTP_401_UNAUTHORIZED)
    serializer = ReviewSerializer(request.user.reviews, many=True)
    return Response(serializer.data)