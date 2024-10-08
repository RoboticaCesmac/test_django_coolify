from rest_framework import serializers
from django.contrib.auth import get_user_model

user_model = get_user_model()


class UserPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ["first_name", "last_name"]


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj) -> str:
        return obj.get_full_name()

    class Meta:
        model = user_model
        fields = ["id", "username", "first_name", "last_name", "full_name"]
        read_only_fields = ["id", "username", "full_name"]


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj) -> str:
        return obj.get_full_name()

    class Meta:
        model = user_model
        fields = ["id", "username", "password", "first_name", "last_name", "full_name"]
        read_only_fields = ["id", "full_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return user_model.objects.create_user(**validated_data)
