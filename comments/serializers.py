from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):  # Class
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def get_is_owner(self, obj):  # Method
        request = self.context['request']
        return request.user == obj.owner

    class Meta:  # Meta Class
        model = Comment
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image',
            'created_at', 'updated_at', 'post', 'content'
            ]


class CommentDetailSerializer(CommentSerializer):
    post = serializers.ReadOnlyField(source='post.id')
