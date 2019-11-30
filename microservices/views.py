from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from microservices.filters import MicroserviceFilter
from microservices.models import Microservice, Author, Tag, Company, Pair
from microservices.serializers import MicroserviceSerializer, AuthorSerializer, TagSerializer, CompanySerializer, \
    MicroserviceReadSerializer, PairSerializer, PairReadSerializer


class MicroserviceViewSet(ModelViewSet):
    serializer_class = MicroserviceSerializer
    queryset = Microservice.objects.all().prefetch_related('author', 'company', 'tag_set')
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = MicroserviceFilter
    ordering_fields = ('name', 'external_id')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if 'ordering' in request.GET:
            if request.GET['ordering'] in ['tags', '-tags']:
                tag_count = 'tag_count'
                if request.GET['ordering'] == '-tags':
                    tag_count = '-tag_count'
                queryset = queryset.annotate(tag_count=Count('tag')).order_by(tag_count)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    @action(detail=True, methods=['get'])
    def microservices(self, request, pk):
        author_obj = Author.get_by_id(pk)
        microservices = self.paginate_queryset(Microservice.objects.filter(author=author_obj))
        return self.get_paginated_response(data=MicroserviceReadSerializer(microservices, many=True).data)


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

    @action(detail=True, methods=['get'])
    def microservices(self, request, pk):
        company_obj = Company.get_by_id(pk)
        microservices = self.paginate_queryset(Microservice.objects.filter(company=company_obj))
        return self.get_paginated_response(data=MicroserviceReadSerializer(microservices, many=True).data)


class TagViewSet(ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class PairViewSet(ModelViewSet):
    serializer_class = PairSerializer
    queryset = Pair.objects.all()

    @action(detail=True, methods=['get'])
    def connections(self, request, pk):
        microservice_obj = Microservice.get_by_id(pk)
        pairs = Pair.objects.filter(
            Q(first_microservice=microservice_obj) | Q(second_microservice=microservice_obj)
        ).distinct()
        return Response({'main_node': microservice_obj.name, 'pairs': [[pair.first_microservice.name, pair.second_microservice.name] for pair in pairs]}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def all_connections(self, request, pk=None):
        pairs = Pair.objects.all().distinct()
        return Response([[pair.first_microservice.name, pair.second_microservice.name] for pair in pairs], status=status.HTTP_200_OK)
