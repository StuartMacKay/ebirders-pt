from django import template

register = template.Library()


@register.simple_tag()
def get_common_name(species, language_code):
    if "common_name" in species.data:
        if language_code in species.data["common_name"]:
            return species.data["common_name"][language_code]
    return species.common_name
