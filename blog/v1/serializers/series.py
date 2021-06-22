from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from user.serializers import BodeUserDetailSerializer
from blog.utils import helpers
from blog.models import *


class SeriesSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    author = BodeUserDetailSerializer(read_only=True)

    class Meta:
        model = Series
        fields = ['author', 'title', 'slug', 'description',  'post_count']
        read_only_fields = ('author', 'post_count')

    def get_posts(self, obj):
        return obj.post.filter(published=True)

    def get_post_count(self, obj):
        return obj.post.filter(published=True).count()

    def validate_slug(self, slug):
        user = self.context['request'].user
        if helpers.check_slug(slug):
            while Series.objects.filter(author=user, slug=slug).exists():
                slug = f'{slug}-{helpers.gen_token()}'
            return slug
        raise serializers.ValidationError(
            _("slug is not valid")
        )


class SeriesDetailSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    author = BodeUserDetailSerializer(read_only=True)

    def get_posts(self, obj):
        from .post import PostSimpleSerializer
        qs = obj.post.filter(published=True)
        serializer = PostSimpleSerializer(instance=qs, many=True)
        return serializer.data

    def get_post_count(self, obj):
        return obj.post.filter(published=True).count()

    class Meta:
        model = Series
        fields = ['author', 'title', 'slug', 'description', 'posts', 'post_count']
        read_only_fields = ('author', 'post_count', 'posts', )

