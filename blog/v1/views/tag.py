from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from blog.models import Post
from django.db.models import Count
from django.contrib.auth import get_user_model
from taggit.models import Tag
from django.db.models import F

User = get_user_model()


class TagCloud(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, user):
        user = User.objects.get(username=user)
        qs = Post.objects.filter(published=True, author=user).values('tags__name').annotate(
            count=Count('tags')).order_by('-count')
        rename_data = [{'tag': tag['tags__name'], 'count': tag['count']} for tag in qs]
        return Response(data={'cloud': rename_data}, status=HTTP_200_OK)
