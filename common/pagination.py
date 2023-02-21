import math

from django.core.paginator import InvalidPage
from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
    _positive_int,
)
from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


class BasePagination(PageNumberPagination):
    """기본 페이징"""

    page_size = 10
    page_size_query_param = "page_size"
    page_query_param = "page"

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """

        page_size = self.get_page_size(request)
        self.page_size = page_size

        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = self.get_page_number(request, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):

        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    (
                        "total_page",
                        math.ceil(self.page.paginator.count / self.page_size),
                    ),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10


class ReplyPagination(CustomLimitOffsetPagination):
    def get_offset(self, request):
        try:
            return _positive_int(
                request.query_params[self.offset_query_param],
            )
        except (KeyError, ValueError):
            return 1

    def get_paginated_response(self, data):

        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    (
                        "total_page",
                        math.ceil((self.count - 1) / self.limit),
                    ),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )
