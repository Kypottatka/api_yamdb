from rest_framework.pagination import PageNumberPagination

PAGE_NUMBER = 10


class CustomPagination(PageNumberPagination):
    page_size = PAGE_NUMBER
