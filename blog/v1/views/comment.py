from rest_framework import permissions
from rest_framework.generics import *
from blog.v1.serializers.comment import *
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from blog.models import *

class CommentView(ListCreateAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_slug = self.kwargs.get('slug')
        user_id = self.kwargs.get('user')
        qs = PostComment.objects.filter(post__slug=post_slug, post__author__username=user_id)
        return qs

    def perform_create(self, serializer):
        post_author = self.kwargs.get('user')
        post_slug = self.kwargs.get('slug')
        post = Post.objects.filter(author__username=post_author, slug=post_slug)
        if not post.exists():
            raise exceptions.ValidationError("post is invalid")
        else:
            post = post.get()
        serializer.save(user=self.request.user, post=post)
