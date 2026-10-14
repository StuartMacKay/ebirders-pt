from django import template

from ..utils import get_country_count

register = template.Library()


@register.filter
def show_country(country):
    return get_country_count() > 1
