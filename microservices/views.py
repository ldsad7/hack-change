import re

from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from webweb import Web

from microservices.filters import MicroserviceFilter
from microservices.models import Microservice, Author, Tag, Company, Pair
from microservices.serializers import MicroserviceSerializer, AuthorSerializer, TagSerializer, CompanySerializer, \
    MicroserviceReadSerializer, PairSerializer, AuthorReadSerializer, CompanyReadSerializer

webweb_file = 'webweb_representation.html'


def draw_graph_and_save_to_file():
    pairs = Pair.objects.all().distinct()
    adjacency = [[pair.first_microservice.name, pair.second_microservice.name] for pair in pairs]

    display = {
        'attachWebwebToElementWithId': None,
        'charge': 2500,
        'colorBy': 'degree',
        'colorPalette': 'Set1',
        'height': 500,
        'linkLength': 200,
        'linkStrength': 0.75,
        'radius': 10,
        'scaleLinkWidth': True,
        'showNodeNames': True,
        'sizeBy': 'weightedDegree',
        'width': 1400,
    }

    with open('tmp.txt', 'w', encoding='utf-8') as f:
        f.write(str(adjacency))
    # draw_graph_and_save_to_file()
    web = Web(adjacency=adjacency, display=display, title="All microservices")
    return web.html, adjacency


def index(request, microservices=None):
    html_code, adjacency = draw_graph_and_save_to_file()
    html_code = re.sub(
        '"networks": {}',
        f'"networks": {{"All microservices": {{"layers": [{{"edgeList": {adjacency}, "nodes": {{}}, "metadata": null}}]}}}}',
        html_code
    )
    html_code = re.sub('#webweb-center {(.*?)}', r'#webweb-center {\1 \n margin-top: 1150px; display:inline-block;}',
                       html_code, flags=re.DOTALL)
    styles = '\n'.join(re.findall('<style>(.*?)</style>', html_code, re.DOTALL))
    # styles += """#webweb-menu-right {display: grid;}\n#webweb-menu-left {display: grid;}"""
    scripts = '\n'.join(re.findall('<script.*?</script>', html_code, re.DOTALL))
    # context = {'html_code': html_code}
    if microservices is None:
        microservices = MicroserviceReadSerializer(Microservice.objects.all().order_by('-modified')[:10],
                                                   many=True).data
    context = {
        'styles': styles,
        'scripts': scripts,
        'authors': AuthorReadSerializer(Author.objects.all(), many=True).data,
        'statuses': [{'key': status[0], 'display_name': status[1]} for status in Microservice.STATUS],
        'companies': CompanyReadSerializer(Company.objects.all(), many=True).data,
        'microservices': microservices
    }
    return render(request, 'microservices/index.html', context)


def add_microservice(request):
    context = {
        'authors': AuthorReadSerializer(Author.objects.all(), many=True).data,
        'statuses': [{'key': status[0], 'display_name': status[1]} for status in Microservice.STATUS],
        'companies': CompanyReadSerializer(Company.objects.all(), many=True).data
    }
    return render(request, 'microservices/add_microservice.html', context)


def redirect_to_main(request):
    body_unicode = request.body.decode('utf-8')
    dct = {pair.split('=')[0]: pair.split('=')[1] for pair in body_unicode.split('&')[:-1]}
    dct['author'] = Author.get_by_id(int(float(dct['author'])))
    dct['company'] = Company.get_by_id(int(float(dct['company'])))
    Microservice.objects.create(**dct)
    return index(request)


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
        return Response({'main_node': microservice_obj.name,
                         'pairs': [[pair.first_microservice.name, pair.second_microservice.name] for pair in pairs]},
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def all_connections(self, request, pk=None):
        pairs = Pair.objects.all().distinct()
        return Response([[pair.first_microservice.name, pair.second_microservice.name] for pair in pairs],
                        status=status.HTTP_200_OK)
