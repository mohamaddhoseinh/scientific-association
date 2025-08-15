from django.urls import path
from .views import (
 ArticleListCreateView, ArticleDetailView,
 ArticleReviewView, MyArticlesView
)

app_name = 'articles'

urlpatterns = [
 path('', ArticleListCreateView.as_view(), name='article_list'),
 path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
 path('<int:pk>/review/', ArticleReviewView.as_view(), name='article_review'),
 path('my-articles/', MyArticlesView.as_view(), name='my_articles'),
]