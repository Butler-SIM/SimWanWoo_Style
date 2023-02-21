import json
import string
from datetime import datetime, date, timedelta
import random

from django.urls import reverse
from django.utils.http import urlencode


class DataParse:
    """"""

    def form_data_parse(self, source, nested_keys):
        mutated = source
        parse_list = []

        for i in range(len(mutated.getlist(f"{nested_keys[0]}"))):
            extracted = {}
            for j in nested_keys:
                extracted[j] = mutated.getlist(j)[i]

            parse_list.append(extracted)

        return parse_list


def reverse_querystring(
    view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None
):
    """Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    """
    base_url = reverse(
        view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app
    )
    if query_kwargs:
        return "{}?{}".format(base_url, urlencode(query_kwargs))
    return base_url
