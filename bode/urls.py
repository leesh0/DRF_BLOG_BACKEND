from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from dj_rest_auth.registration.views import VerifyEmailView, RegisterView

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Personal
urlpatterns += [
    path('api/', include('user.urls')),
    path('api/', include('blog.urls'))
]

# setting yasg
urlpatterns += [url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), ]

# Setting Media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# setting Silk
if settings.DEBUG:
    urlpatterns += [url(r'^silk/', include('silk.urls', namespace='silk'))]
