from django.urls import path, re_path, include

urlpatterns = [
    path('v1/blog/', include("blog.v1.urls")),
]
