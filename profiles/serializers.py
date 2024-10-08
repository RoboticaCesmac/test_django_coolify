from rest_framework import serializers
from accounts.serializers import UserProfileSerializer
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    age = serializers.IntegerField(read_only=True)

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user_serializer = UserProfileSerializer(
            instance=instance.user, data=user_data, partial=True
        )
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return super().update(instance, validated_data)

    class Meta:
        model = Profile
        fields = ["user", "birth_date", "age", "created_at", "updated_at"]
        read_only_fields = ["user", "created_at", "updated_at"]
