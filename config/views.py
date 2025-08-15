from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'message': 'خوش آمدید به API انجمن علمی',
        'endpoints': {
            'accounts': {
                'register': reverse('accounts:register', request=request, format=format),
                'login': reverse('accounts:login', request=request, format=format),
                'profile': reverse('accounts:profile', request=request, format=format),
                'users': reverse('accounts:user_list', request=request, format=format),
            },
            'news': {
                'list': reverse('news:news_list', request=request, format=format),
                'categories': reverse('news:category_list', request=request, format=format),
            },
            'events': {
                'list': reverse('events:event_list', request=request, format=format),
                'my-registrations': reverse('events:my_registrations', request=request, format=format),
            },
            'articles': {
                'list': reverse('articles:article_list', request=request, format=format),
                'my-articles': reverse('articles:my_articles', request=request, format=format),
            }
        },
        'documentation': {
            'swagger': reverse('schema-swagger-ui', request=request, format=format),
            'redoc': reverse('schema-redoc', request=request, format=format),
        }
    })