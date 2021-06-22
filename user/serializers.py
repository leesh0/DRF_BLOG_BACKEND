from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from .utils.helpers import email2username, username_token
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.socialaccount.helpers import complete_social_login
    from allauth.socialaccount.models import SocialAccount
    from allauth.socialaccount.providers.base import AuthProcess
    from allauth.utils import email_address_exists, get_username_max_length
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')

from allauth.account.urls import *

User = get_user_model()


class BodeUserDetailSerializer(UserDetailsSerializer):
    class Meta:
        model = User
        extra_fields = [
            User.USERNAME_FIELD,
            'avatar', 'nickname', 'introduce', 'blog_name', 'twitter', 'github'
        ]
        fields = (*extra_fields,)

    def validate_username(self, username):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        if username == user.username:
            return username
        else:
            result = super().validate_username(username)
            return result

    def validate_nickname(self, nickname):
        if len(nickname) < 3:
            raise ValidationError("nickname의 길이가 너무 짧습니다.")
        else:
            return nickname


    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        ret = super().to_representation(instance)
        return {'user': ret}


class BodeRegisterSerializer(RegisterSerializer):

    def custom_user(self, user, data):
        want_name = email2username(data['email'])
        name = want_name
        while User.objects.filter(username=name).exists():
            name = f'{want_name}_{username_token()}'
        data['username'] = name
        user.user_id = name
        return data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        self.custom_user(user, self.cleaned_data)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


from allauth.account.utils import complete_signup
