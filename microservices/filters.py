from django.db.models import Q
from django_filters import rest_framework as filters

from microservices.models import Microservice


class MicroserviceFilter(filters.FilterSet):
    name = filters.CharFilter('name', 'icontains')
    status = filters.MultipleChoiceFilter(choices=Microservice.STATUS)
    author_id = filters.BaseInFilter('author_id')
    external_id = filters.BaseInFilter('external_id')
    start_date_gt = filters.DateFilter('start_date', 'gt')
    start_date_gte = filters.DateFilter('start_date', 'gte')
    start_date_eq = filters.DateFilter('start_date', 'iexact')
    start_date_lt = filters.DateFilter('start_date', 'lt')
    start_date_lte = filters.DateFilter('start_date', 'lte')
    end_date_gt = filters.DateFilter('end_date', 'gt')
    end_date_gte = filters.DateFilter('end_date', 'gte')
    end_date_eq = filters.DateFilter('end_date', 'iexact')
    end_date_lt = filters.DateFilter('end_date', 'lt')
    end_date_lte = filters.DateFilter('end_date', 'lte')
    company_id = filters.BaseInFilter('company_id')
    is_active = filters.BooleanFilter('is_active')
    is_deleted = filters.BooleanFilter('is_deleted')
    tags = filters.BaseInFilter('tag')
