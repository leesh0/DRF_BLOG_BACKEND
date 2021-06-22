from django.urls import path, re_path, include
from .views import series, post, comment, upload, tag
from django.urls import register_converter
from django.urls.converters import StringConverter


class HangulSlugConverter(StringConverter):
    regex = '[-\w]+'


register_converter(HangulSlugConverter, 'unislug')

urlpatterns = [
    # public
    path('series/', series.SeriesView.as_view(), name="series_list_view"),
    path('posts/', post.PostView.as_view(), name="post_list_view"),
    path('@<slug:user>/tagcloud/', tag.TagCloud.as_view()),

    # personal
    # Upload
    path('upload/', upload.ImageUploadView.as_view(), name="user_image_uploader"),

    # Series
    path('@<slug:author>/series/', series.UserSeriesView.as_view(), name="user_series_view"),
    path('@<slug:author>/series/<unislug:slug>', series.UserDetailSeriesView.as_view(), name="user_series_detail_view"),

    # Posts
    path('@<slug:author>/posts/', post.UserPostView.as_view(), name="user_posts_view"),
    path('@<slug:author>/posts/<unislug:slug>', post.UserDetailPostView.as_view(), name="user_post_detail_view"),
    path('@<slug:author>/posts/<unislug:slug>/like', post.PostLikeView.as_view(), name="user_post_like_view"),

    # Comment
    path('@<slug:user>/posts/<unislug:slug>/comments', comment.CommentView.as_view(), name="user_post_comment_view")
]
