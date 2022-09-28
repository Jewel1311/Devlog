from django.core.exceptions import ValidationError
from .utils import extract_tags


def tag_validation(tag):
    tag_list = extract_tags(tag)
    if len(tag_list) > 3:
        raise ValidationError("Maximum of 3 tags are allowed")
    
