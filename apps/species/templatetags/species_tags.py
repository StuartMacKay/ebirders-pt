from django import template

register = template.Library()


@register.simple_tag()
def get_common_name(species, language_code):
    return species.data["common_name"][language_code]
