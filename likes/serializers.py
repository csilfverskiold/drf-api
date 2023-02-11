from django.db import IntegrityError
from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):  # Class
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['id', 'created_at', 'owner', 'post']

    """Method added to prevent users from making duplicate likes"""
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'possible duplicate'
            })
