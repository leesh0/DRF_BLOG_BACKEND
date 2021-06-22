from django.contrib.auth import get_user_model
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView, SocialAccountDisconnectView
from allauth.socialaccount.models import SocialAccount
from rest_framework.exceptions import MethodNotAllowed, NotFound
from rest_framework.parsers import *
from allauth.socialaccount.adapter import get_adapter as get_social_adapter
from rest_framework.exceptions import *
from allauth.socialaccount import signals
from rest_framework.response import Response
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import *
from .serializers import BodeUserDetailSerializer
import requests
from allauth.socialaccount import app_settings

User = get_user_model()


class GHAdapter(GitHubOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        headers = {"Authorization": "token {}".format(token.token)}
        resp = requests.get(self.profile_url, headers=headers)
        resp.raise_for_status()
        extra_data = resp.json()
        if app_settings.QUERY_EMAIL and not extra_data.get("email"):
            extra_data["email"] = self.get_email(headers)
        social_user = self.get_provider().sociallogin_from_response(request, extra_data)

        return social_user


class GithubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    callback_url = 'http://192.168.0.3:3000/auth/github'
    client_class = OAuth2Client

class GithubDisconnectView(SocialAccountDisconnectView):
    def post(self, request, *args, **kwargs):
        accounts = self.get_queryset()
        account = accounts.first()
        if not account:
            raise NotFound

        # get_social_adapter(self.request).validate_disconnect(account, accounts)
        account_user = User.objects.filter(id=self.request.user.id).first()
        account_user.delete()
        signals.social_account_removed.send(
            sender=SocialAccount,
            request=self.request,
            socialaccount=account,
        )

        return Response(self.get_serializer(account).data)


class UserDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BodeUserDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    parser_classes = [FormParser, MultiPartParser]

    def get_object(self):
        return User.objects.get(id=self.request.user.id)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

class PublicUserDetailView(RetrieveAPIView):
    serializer_class = BodeUserDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self):
        username = self.kwargs.get('username')
        if not username:
            raise ValidationError("username is not existed")
        return User.objects.filter(username=username).first()
