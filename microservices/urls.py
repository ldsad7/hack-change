from django.urls import path, include
from rest_framework.routers import DefaultRouter

from microservices.views import MicroserviceViewSet, AuthorViewSet, TagViewSet

api_router = DefaultRouter()
api_router.register('microservices', MicroserviceViewSet, 'microservices')
api_router.register('authors', AuthorViewSet, 'authors')
api_router.register('tags', TagViewSet, 'tags')

urlpatterns = [
    path('', include(api_router.urls)),
]
