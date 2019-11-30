from rest_framework import serializers

from microservices.models import Microservice, Author, Tag, Company, Pair


class MicroserviceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Microservice

    def to_representation(self, instance):
        return MicroserviceReadSerializer(instance).data


class MicroserviceReadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Microservice
        # read_only_fields = fields

    author = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    @staticmethod
    def get_tags(instance: Microservice):
        return TagReadSerializer(instance.tag_set, many=True).data

    @staticmethod
    def get_author(instance: Microservice):
        return AuthorReadSerializer(instance.author).data

    @staticmethod
    def get_company(instance: Microservice):
        return CompanyReadSerializer(instance.company).data

    @staticmethod
    def get_status(instance: Microservice):
        return {
            "key": instance.status,
            "display": instance.get_status_display()
        }


class ShortMicroserviceReadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name'
        )
        model = Microservice
        read_only_fields = fields


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Author

    def to_representation(self, instance):
        return AuthorReadSerializer(instance).data


class AuthorReadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Author
        # read_only_fields = fields


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Company

    def to_representation(self, instance):
        return CompanyReadSerializer(instance).data


class CompanyReadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Company
        # read_only_fields = fields


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag

    def to_representation(self, instance):
        return TagReadSerializer(instance).data


class TagReadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'description'
        )
        model = Tag
        read_only_fields = fields


class PairSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Pair

    def to_representation(self, instance):
        return PairReadSerializer(instance).data


class PairReadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Pair
        # read_only_fields = fields

    first_microservice = serializers.SerializerMethodField()
    second_microservice = serializers.SerializerMethodField()

    @staticmethod
    def get_first_microservice(instance: Pair):
        return ShortMicroserviceReadSerializer(instance.first_microservice).data

    @staticmethod
    def get_second_microservice(instance: Pair):
        return ShortMicroserviceReadSerializer(instance.second_microservice).data
