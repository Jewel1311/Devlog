from django.template.defaulttags import register

@register.filter
def get_liked(dictionary, key):
    return dictionary.get(key)