from rest_framework import serializers
from .models import Like


class LikeSerializer(serializers.ModelSerializer):  # Class
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:  # Meta Class
        model = Like
        fields = ['id', 'owner', 'post', 'created_at']
