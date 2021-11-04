from django.contrib import admin
from django.urls import path, include

# Import for rest_framework
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static

# Import for graphQL
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.decorators import jwt_cookie
from .schema import schema


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.ourapp.com/policies/terms/",
      contact=openapi.Contact(email="contact@findTutor.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('findTutor/', include('findTutor.urls')),
    path('auth/', include('authentication.urls')),
    path('social-auth/', include('socialAuth.urls')),
    path('search/', include('search.urls')),
    path('websocket/', include('websocket.urls')),

    # for graphQL
    path('graphql/', csrf_exempt(jwt_cookie(GraphQLView.as_view(graphiql=True, schema=schema)))),
]

urlpatterns += [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

