from rest_framework import permissions
from rest_framework.generics import *
from blog.v1.serializers.post import *
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from rest_framework.parsers import *
from django.db.models import Count
from blog.models import *
from blog.pagination import BodePagination
from django.db.models import Q


class PostView(ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.filter(published=True)
    parser_classes = [FormParser, MultiPartParser]
    pagination_class = BodePagination

    def get_queryset(self):
        params = self.request.query_params
        order_by = params.get('type')
        tag = params.get('tag')
        if tag:
            query = Post.objects.filter(published=True, tags__name__icontains=tag)
        else:
            query = Post.objects.filter(published=True)
        if order_by and order_by == 'trend':
            return query.prefetch_related('like').annotate(count=Count('like')).order_by(
                'count')
        else:
            return query.order_by('-created')

    def get_serializer_context(self):
        origin = super().get_serializer_context()
        origin.update({'kwargs': self.kwargs})
        return origin

    def perform_create(self, serializer):
        series_slug = self.request.data.get('series')
        if not series_slug:
            serializer.save(author=self.request.user)
            return
        series = Series.objects.filter(author=self.request.user, slug=series_slug)
        if not series.exists():
            raise exceptions.ValidationError("series is invalid")
        else:
            series = series.get()
        serializer.save(author=self.request.user, series=series)


class UserPostView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = BodePagination

    def get_queryset(self):
        params = self.request.query_params
        author = self.kwargs.get('author')
        tag = params.get('tag')
        if tag:
            query = Post.objects.filter(author__username=author, published=True, tags__name__icontains=tag)
        else:
            query = Post.objects.filter(author__username=author, published=True)

        return query \
            .select_related('series', 'author', 'series__author').order_by('-created')


class UserDetailPostView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "author"

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset)

    def get_queryset(self):
        author = self.kwargs.get('author')
        slug = self.kwargs.get('slug')
        qs = Post.objects.filter(author__username=author, slug=slug) \
            .select_related('author') \
            .prefetch_related('like')
        print(author, slug,qs)
        return qs


class PostLikeView(CreateAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_author = self.kwargs.get('author')
        post_slug = self.kwargs.get('slug')
        return PostLike.objects.filter(post__author__username=post_author, post__slug=post_slug, user=self.request.user)

    def perform_create(self, serializer):
        queryset = self.get_queryset()
        if queryset.exists():
            queryset.delete()
            return None
        post_author = self.kwargs.get('author')
        post_slug = self.kwargs.get('slug')
        post = Post.objects.get(author__username=post_author, slug=post_slug)
        serializer.save(user=self.request.user, post=post)
        return True

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.perform_create(serializer):
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'message': 'success'}, status=status.HTTP_205_RESET_CONTENT)
