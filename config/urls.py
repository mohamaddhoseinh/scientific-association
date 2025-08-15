from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import api_root  # اضافه شد
from django.http import JsonResponse # این خط اضافه شد
from django.shortcuts import render # این خط اضافه شد

# تنظیمات Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Scientific Association API",
        default_version='v1',
        description="API برای سیستم انجمن علمی دانشگاه",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@scientificassociation.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def home_view(request):
    """صفحه اصلی سیستم"""
    if request.content_type == 'application/json' or 'api' in request.path:
        return JsonResponse({
            'message': 'خوش آمدید به سیستم انجمن علمی',
            'version': '1.0',
            'endpoints': {
                'admin': '/admin/',
                'api_docs': '/swagger/',
                'accounts': '/api/accounts/',
                'news': '/api/news/',
                'events': '/api/events/',
                'articles': '/api/articles/',
            }
        })
    else:
        return render(request, 'home.html')
    
urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    
    # API Root
    path('api/', api_root, name='api-root'),
    
    # API URLs
    path('api/accounts/', include('accounts.urls')),
    path('api/news/', include('news.urls')),
    path('api/events/', include('events.urls')),
    path('api/articles/', include('articles.urls')),
    
    
    # Swagger Documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# فایل‌های استاتیک و مدیا در حالت توسعه
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)