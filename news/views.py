from rest_framework import generics, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, News
from .serializers import (
    CategorySerializer, NewsListSerializer, 
    NewsCreateSerializer, NewsDetailSerializer
)
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class NewsListCreateView(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_published']
    search_fields = ['title', 'content']
    ordering_fields = ['publish_date', 'created_at']
    ordering = ['-publish_date']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = News.objects.all()
        if not self.request.user.is_authenticated or not self.request.user.is_admin():
            queryset = queryset.filter(is_published=True)
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewsCreateSerializer
        return NewsListSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer
    permission_classes = [IsAuthorOrReadOnly]
    
    def get_queryset(self):
        queryset = News.objects.all()
        if not self.request.user.is_authenticated or not self.request.user.is_admin():
            queryset = queryset.filter(is_published=True)
        return queryset

class NewsPublishView(generics.UpdateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        news = self.get_object()
        if not request.user.is_admin():
            return Response({"detail": "شما اجازه انتشار خبر ندارید"}, status=403)
        
        news.is_published = True
        news.save()
        return Response({"detail": "خبر با موفقیت منتشر شد"})