from django.core.exceptions import ValidationError
from .utils import extract_tags


def tag_validation(tag):
    tag_list = extract_tags(tag)
    if len(tag_list) > 3:
        raise ValidationError("Maximum of 3 tags are allowed")
    
def validate_image(img):
    size = img.size
    format = img.name.split(".")[-1]
    avaible_formats = [
        'png',
        'jpg',
        'jpeg'
    ]
    if size > 4194304:
        raise ValidationError("Image size must be less than 4MB")
    if format not in avaible_formats:
        raise ValidationError("Invalid image extension")
    
    return img

