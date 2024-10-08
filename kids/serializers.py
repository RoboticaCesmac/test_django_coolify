from rest_framework import serializers

from kids.models import Kid


class KidSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)
    father = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Kid
        fields = [
            "id",
            "father",
            "name",
            "birth_date",
            "age",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
