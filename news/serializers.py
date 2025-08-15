from rest_framework import serializers
from .models import Category, News
from accounts.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class NewsListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'image', 'author', 
                 'category', 'is_published', 'publish_date', 'created_at')

class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('title', 'content', 'image', 'category')
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class NewsDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = News
        fields = '__all__'