from django.urls import path
from .views import (
 CategoryListCreateView, CategoryDetailView,
 NewsListCreateView, NewsDetailView, NewsPublishView
)

app_name = 'news'

urlpatterns = [
 path('categories/', CategoryListCreateView.as_view(), name='category_list'),
 path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
 path('', NewsListCreateView.as_view(), name='news_list'),
 path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
 path('<int:pk>/publish/', NewsPublishView.as_view(), name='news_publish'),
]