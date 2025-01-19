from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from books.views import AuthorViewSet, BookViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

# Настройка Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Book API",
        default_version='v1',
        description="API documentation for the book library",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@bookapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
