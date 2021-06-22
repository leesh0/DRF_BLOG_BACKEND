from django.urls import path
from dj_rest_auth.registration.views import VerifyEmailView, RegisterView
from dj_rest_auth.registration.views import SocialAccountDisconnectView
from .views import *
from django.urls import path, re_path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', RegisterView.as_view(), name='rest_register'),
    path('registration/verify-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('social/github/', GithubLogin.as_view(), name='resend-email-confirmation'),
    path('user', UserDetailView.as_view(), name="user_detail_view"),
    path('user/<str:username>/', PublicUserDetailView.as_view()),
    # path('disconnect/', GithubDisconnectView.as_view(), name="disconnect_view"),
    # This url is used by django-allauth and empty TemplateView is
    # defined just to allow reverse() call inside app, for example when email
    # with verification link is being sent, then it's required to render email
    # content.

    # account_confirm_email - You should override this view to handle it in
    # your API client somehow and then, send post to /verify-email/ endpoint
    # with proper key.
    # If you don't want to use API on that step, then just use ConfirmEmailView
    # view from:
    # django-allauth https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py
    re_path(
        r'^registration/account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
        name='account_confirm_email',
    ),
]
