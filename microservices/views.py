from rest_framework.viewsets import ModelViewSet

from microservices.models import Microservice, Author, Tag
from microservices.serializers import MicroserviceSerializer, AuthorSerializer, TagSerializer


class MicroserviceViewSet(ModelViewSet):
    serializer_class = MicroserviceSerializer
    queryset = Microservice.objects.all()


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
