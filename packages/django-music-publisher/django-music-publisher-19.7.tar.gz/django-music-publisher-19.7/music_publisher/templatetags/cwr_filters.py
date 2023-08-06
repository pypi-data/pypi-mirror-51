"""Filters used in generation of CWR files.

Their goal is to format the incoming data to the right fixed-length
format, as well as do some basic validation.
"""

from django import template
from datetime import date, time
from decimal import Decimal, ROUND_HALF_UP
from django.utils.html import mark_safe
from music_publisher import const, models


register = template.Library()


@register.filter(name='rjust')
def rjust(value, length):
    """Format general numeric fields."""

    if value is None or value == '':
        value = '0'
    else:
        value = str(value)
    value = value.rjust(length, '0')
    return value


@register.filter(name='ljust')
def ljust(value, length):
    """Format general alphanumeric fields."""

    if value is None:
        value = ''
    else:
        value = str(value)
    value = value.ljust(length, ' ')
    return value


@register.filter(name='soc')
def soc(value):
    """Format society fields."""

    if not value:
        return '   '
    value = value.rjust(3, '0')
    return value

@register.filter(name='prshare')
def prshare(value):
    """Format and validate fields containing shares."""
    value = value or 0
    value = (value * Decimal(5000)).quantize(
        Decimal('1.'), rounding=ROUND_HALF_UP)
    value = int(value)
    return '{:05d}'.format(value)


@register.filter(name='mrshare')
def mrshare(value):
    """Format and validate fields containing shares."""

    value = value or 0
    value = (value * Decimal(10000)).quantize(
        Decimal('1.'), rounding=ROUND_HALF_UP)
    value = int(value)
    return '{:05d}'.format(value)

@register.filter(name='perc')
def perc(value):
    """Display shares as human-readable string."""

    value = Decimal(value) / Decimal('100')
    return '{}%'.format(value)

@register.filter(name='soc_name')
def soc_name(value):
    """Display society name"""

    value = value.strip()
    return const.SOCIETY_DICT.get(value, '')

@register.filter(name='capacity')
def capacity(value):
    """Display capacity"""

    value = value.strip()
    obj = models.WriterInWork(capacity=value)
    return obj.get_capacity_display()
