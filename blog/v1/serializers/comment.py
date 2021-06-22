from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from blog.utils import helpers
from blog.models import *
from user.serializers import BodeUserDetailSerializer


class PostCommentSerializer(serializers.ModelSerializer):
    user = BodeUserDetailSerializer(read_only=True)

    class Meta:
        model = PostComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'post', 'user')
