from rest_framework import serializers

from ..models import Post


class PostSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'pk', 'title', 'text', 'active',
            'created', 'updated', 'user_id',
            'icon'
        )
        read_only_fields = fields

    def get_user_id(self, obj: Post):
        return obj.user.pk
