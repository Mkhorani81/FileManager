from rest_framework.pagination import PageNumberPagination


class FileAdminPagination(PageNumberPagination):
    """
    Custom pagination class for the paginated file when list them
    """
    page_size = 2
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 20

