from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.permissions import *
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser
from rest_framework.response import Response
from blog.utils.helpers import pk_gen
import uuid


class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated, ]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, filename=None):
        file_obj = request.FILES['file']
        file_ext = file_obj.name.split('.')[-1]
        fname = f'{pk_gen()}.{file_ext}'
        image = default_storage.save(f'blog/{fname}', ContentFile(file_obj.read()))
        url = default_storage.url(image)
        image_url = request.build_absolute_uri(url)
        return Response({'name': file_obj.name, 'url': image_url})
        # fname =  uuid.uuid4().hex + f".{ftype}"
