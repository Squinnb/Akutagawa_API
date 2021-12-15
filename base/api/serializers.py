from rest_framework.serializers import ModelSerializer, StringRelatedField
from base.models import User, Book, Review

class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
     
class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
    user = StringRelatedField(many=False)
    
    # def create(self, validated_data):
    #     return Review.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     return instance