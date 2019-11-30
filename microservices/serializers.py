from rest_framework import serializers

from microservices.models import Microservice, Author, Tag


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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag

    def to_representation(self, instance):
        return TagReadSerializer(instance).data


class TagReadSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag
        # read_only_fields = fields
