"""Backend-agnostic communication-related routines (preprocessing of requests,
formatting of responses)."""
from datetime import datetime

import financeager.httprequests
import financeager.localserver
from . import PERIOD_DATE_FORMAT
from .listing import prettify, Listing
from .entries import prettify as prettify_element
from .entries import CategoryEntry
from .exceptions import PreprocessingError


def module(name):
    """Return the client module corresponding to the backend specified by 'name'
    ('flask' or 'none').
    """
    frontend_modules = {
        "flask": "httprequests",
        "none": "localserver",
    }
    return getattr(financeager, frontend_modules[name])


def run(proxy,
        command,
        default_category=CategoryEntry.DEFAULT_NAME,
        date_format=None,
        stacked_layout=False,
        entry_sort=CategoryEntry.BASE_ENTRY_SORT_KEY,
        category_sort=Listing.CATEGORY_ENTRY_SORT_KEY,
        **kwargs):
    """Run a command on the given proxy. The kwargs are preprocessed and passed
    on. The server response is formatted and returned. If the response does not
    contain any of the fields 'elements', 'element', or 'periods', the empty
    string is returned.

    :raises: CommunicationError, InvalidRequest
    :return: str
    """
    _preprocess(kwargs, date_format)
    response = proxy.run(command, **kwargs)

    eid = response.get("id")
    if eid is not None:
        verb = {
            "add": "Added",
            "update": "Updated",
            "rm": "Removed",
            "copy": "Copied"
        }[command]
        return "{} element {}.".format(verb, eid)

    elements = response.get("elements")
    if elements is not None:
        CategoryEntry.BASE_ENTRY_SORT_KEY = entry_sort
        CategoryEntry.DEFAULT_NAME = default_category
        Listing.CATEGORY_ENTRY_SORT_KEY = category_sort
        return prettify(elements, stacked_layout)

    element = response.get("element")
    if element is not None:
        CategoryEntry.DEFAULT_NAME = default_category
        return prettify_element(
            element, recurrent=kwargs.get("table_name") == "recurrent")

    periods = response.get("periods")
    if periods is not None:
        return "\n".join([p for p in periods])

    return ""


def _preprocess(data, date_format=None):
    """Preprocess data to be passed to server (e.g. convert date format, parse
    'filters' options passed with print command). Raises PreprocessError if
    preprocessing failed.
    """
    date = data.get("date")
    # recovering offline data does not bring any date format because the data
    # has already been converted
    if date is not None and date_format is not None:
        try:
            date = datetime.strptime(date,
                                     date_format).strftime(PERIOD_DATE_FORMAT)
            data["date"] = date
        except ValueError:
            raise PreprocessingError("Invalid date format.")

    filter_items = data.get("filters")
    if filter_items is not None:
        # convert list of "key=value" strings into dictionary
        parsed_items = {}
        try:
            for item in filter_items:
                key, value = item.split("=")
                parsed_items[key] = value.lower()

            try:
                # Substitute category default name
                if parsed_items["category"] == CategoryEntry.DEFAULT_NAME:
                    parsed_items["category"] = None
            except KeyError:
                # No 'category' field present
                pass

            data["filters"] = parsed_items
        except ValueError:
            # splitting returned less than two parts due to missing separator
            raise PreprocessingError("Invalid filter format: {}".format(item))
