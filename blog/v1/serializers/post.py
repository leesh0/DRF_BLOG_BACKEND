from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from blog.utils import helpers
from blog.models import *
from user.serializers import BodeUserDetailSerializer
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    from .series import SeriesSerializer
    series = SeriesSerializer(read_only=True)
    author = BodeUserDetailSerializer(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Post
        exclude = ('id',)
        read_only_fields = ('author', 'updated', 'created')

    @staticmethod
    def get_like_count(obj):
        return obj.like.count()

    @staticmethod
    def get_comment_count(obj):
        return obj.comments.count()

    def validate_slug(self, slug):
        user = self.context['request'].user
        if helpers.check_slug(slug):
            while Post.objects.filter(author=user, slug=slug).exists():
                slug = f'{slug}-{helpers.gen_token()}'
            return slug
        raise serializers.ValidationError(
            _("slug is not valid")
        )


class PostDetailSerializer(TaggitSerializer, serializers.ModelSerializer):
    from .series import SeriesDetailSerializer
    series = SeriesDetailSerializer(read_only=True)
    author = BodeUserDetailSerializer(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    tags = TagListSerializerField()

    @staticmethod
    def get_like_count(obj):
        return obj.like.count()

    class Meta:
        model = Post
        exclude = ('id',)
        read_only_fields = ('author', 'updated', 'created')


class PostSimpleSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = BodeUserDetailSerializer(read_only=True)
    tags = TagListSerializerField()
    like_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['author', 'title', 'slug', 'description', 'created', 'tags', 'thumbnail', 'like_count']
        read_only_fields = ('like_count',)

    @staticmethod
    def get_like_count(obj):
        return obj.like.count()


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('post', 'user')
        read_only_fields = ('user', 'post')
