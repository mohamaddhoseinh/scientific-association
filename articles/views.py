from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Q
from .models import Article
from .serializers import (
    ArticleListSerializer, ArticleCreateSerializer,
    ArticleDetailSerializer, ArticleReviewSerializer
)

class ArticleListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Article.objects.all()
        
        # فیلتر براساس وضعیت
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # کاربران عادی فقط مقالات تایید شده را ببینند
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='approved')
        elif not self.request.user.is_admin():
            # کاربران لاگین شده مقالات خودشان و مقالات تایید شده را ببینند
            queryset = queryset.filter(
                Q(author=self.request.user) | Q(status='approved')
            )
        
        return queryset.order_by('-submission_date')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ArticleCreateSerializer
        return ArticleListSerializer

class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Article.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='approved')
        elif not self.request.user.is_admin():
            queryset = queryset.filter(
                Q(author=self.request.user) | Q(status='approved')
            )
        return queryset
    
    def update(self, request, *args, **kwargs):
        article = self.get_object()
        if article.author != request.user and not request.user.is_admin():
            return Response(
                {"detail": "شما اجازه ویرایش این مقاله را ندارید"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # اگر مقاله تایید شده باشد، نمی‌توان آن را ویرایش کرد
        if article.status == 'approved' and not request.user.is_admin():
            return Response(
                {"detail": "مقاله تایید شده قابل ویرایش نیست"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return super().update(request, *args, **kwargs)

class ArticleReviewView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        if not request.user.is_admin():
            return Response(
                {"detail": "فقط مدیران می‌توانند مقالات را بررسی کنند"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

class MyArticlesView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Article.objects.filter(
            author=self.request.user
        ).order_by('-submission_date')