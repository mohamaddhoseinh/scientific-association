from rest_framework import serializers
from .models import Article
from django.utils import timezone
from accounts.serializers import UserSerializer
from news.serializers import CategorySerializer

class ArticleListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Article
        fields = ('id', 'title', 'abstract', 'author', 'category',
                 'status', 'submission_date')

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'abstract', 'file', 'category')
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    
    class Meta:
        model = Article
        fields = '__all__'

class ArticleReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('status', 'review_comment')
    
    def update(self, instance, validated_data):
        instance.reviewer = self.context['request'].user
        instance.reviewed_date = timezone.now()
        return super().update(instance, validated_data)