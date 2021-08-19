from rest_framework import pagination
from rest_framework.response import Response


class PageNumberPagination(pagination.PageNumberPagination):
    """
    Default pagination class with metadata in response's header.
    """
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'page_size'
    page_query_param = 'page'

    def get_paginated_response(self, data):
        """
        Build response with pagination metadata in header.
        """
        response = Response(data)
        response['page_next'] = self.get_next_link()
        response['page_count'] = self.page.paginator.count
        response['page_previous'] = self.get_previous_link()
        return response
