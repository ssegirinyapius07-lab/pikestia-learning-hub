"""Shared, database-backed search helpers for Pikestia.

Search is deliberately deterministic: every query term must match somewhere in
the selected fields, and title matches are ordered ahead of incidental matches.
"""
import re

from django.db.models import Case, IntegerField, Q, Value, When


_TERM_PATTERN = re.compile(r'[\w+#.-]+', re.UNICODE)


def query_terms(query):
    """Return a small, safe set of useful words from a visitor's query."""
    return _TERM_PATTERN.findall((query or '').strip().casefold())[:8]


def filter_by_terms(queryset, query, fields):
    """Require every search term to occur in at least one of the selected fields."""
    terms = query_terms(query)
    if not terms:
        return queryset.none()

    for term in terms:
        term_match = Q()
        for field in fields:
            term_match |= Q(**{f'{field}__icontains': term})
        queryset = queryset.filter(term_match)

    return queryset


def with_title_relevance(queryset, query, title_field='title'):
    """Rank exact and prefix title matches before broader text matches."""
    phrase = (query or '').strip()
    if not phrase:
        return queryset

    return queryset.annotate(
        _search_title_rank=Case(
            When(**{f'{title_field}__iexact': phrase}, then=Value(0)),
            When(**{f'{title_field}__istartswith': phrase}, then=Value(1)),
            When(**{f'{title_field}__icontains': phrase}, then=Value(2)),
            default=Value(3),
            output_field=IntegerField(),
        )
    )
