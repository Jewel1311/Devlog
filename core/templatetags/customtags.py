from django.template.defaulttags import register

@register.filter
def get_dict(dictionary, key):
    return dictionary.get(key)


