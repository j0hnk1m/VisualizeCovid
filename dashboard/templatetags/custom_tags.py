from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    if key:
        return dictionary.get(key)
