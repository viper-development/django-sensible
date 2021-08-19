from rest_framework import filters


class LimitedSearchFilter(filters.SearchFilter):
    """
    Search backend with an item limit.
    Default to 10.

    Note: The use of pagination is preferred.
    """
    filter_limit = 10

    def filter_queryset(self, request, queryset, view):
        """
        The queryset is sliced and limited only when using the search backend
        (For now, only when using a GET request).
        """
        queryset = super().filter_queryset(request, queryset, view)

        return (queryset[:self.filter_limit] if 'search' in request.GET
                else queryset)
