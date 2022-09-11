from rest_framework.pagination import PageNumberPagination


class CustomCandidatePagination(PageNumberPagination):
    """This is a custom paginator for Candidates."""

    page_size = 25
    page_size_query_param = "page_size"
