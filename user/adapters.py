from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from allauth.account.utils import user_field
from django.contrib.auth import get_user_model
from .utils.helpers import pk_gen
import threading
import uuid
import requests

# class BackgroundEmailSendingAccountAdapter(DefaultAccountAdapter):
#
#     def send_mail(self, template_prefix, email, context):
#         print(context)
#         mailing_thread = threading.Thread(
#             target=super(BackgroundEmailSendingAccountAdapter, self).send_mail,
#             args=(template_prefix, email, context)
#         )
#         mailing_thread.start()
#
# class BodeSocialAccountAdapter(DefaultSocialAccountAdapter):
#     def save_user(self, request, sociallogin, form=None):
#         pass

User = get_user_model()


class BodeAccountAdapter(DefaultSocialAccountAdapter):
    # def pre_social_login(self, request, sociallogin):
    #     user = sociallogin.user
    #     social_data = SocialAccount.objects.get(user=user)
    #     print(social_data.get_avatar_url())

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        social_account = SocialAccount.objects.get(user=user)
        avatar = social_account.get_avatar_url()
        avatar_file = requests.get(avatar)
        if avatar_file.status_code != 200:
            return user
        avatar_bin = avatar_file.content
        ftype = avatar_file.headers.get('content-type', 'images/jpg').split("/")[-1]
        fname = uuid.uuid4().hex + f".{ftype}"
        _avatar = default_storage.save(f'avatar/{fname}', ContentFile(avatar_bin))
        user_model = User.objects.filter(id=user.id)
        user_model.update(avatar=_avatar)
        return user
