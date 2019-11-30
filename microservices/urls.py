from django.urls import path, include
from rest_framework.routers import DefaultRouter

from microservices.views import MicroserviceViewSet, AuthorViewSet, TagViewSet, CompanyViewSet, PairViewSet

api_router = DefaultRouter()
api_router.register('microservices', MicroserviceViewSet, 'microservices')
api_router.register('authors', AuthorViewSet, 'authors')
api_router.register('tags', TagViewSet, 'tags')
api_router.register('companies', CompanyViewSet, 'companies')
api_router.register('pairs', PairViewSet, 'pairs')

urlpatterns = [
    path('', include(api_router.urls)),
]
