# myapp/admin.py
from django.contrib import admin
from .models import BodeUser

admin.site.register(BodeUser)  # 기본 ModelAdmin으로 등록
