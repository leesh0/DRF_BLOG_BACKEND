from rest_framework.pagination import PageNumberPagination

class BodePagination(PageNumberPagination):
    page_size = 20
