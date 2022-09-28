import re
import readtime
from . models import Tags

def extract_tags(tag):
    tag_set = set(re.findall(r"(\#\w+)", tag))
    tag_list = list(tag_set)
    return tag_list

def get_read_time(body):
    result = readtime.of_text(body)
    return result.minutes


def save_tags(tags):
    tag_list = extract_tags(tags)
    post_tags = [] #list of tag id is created
    for tag in tag_list:
        object = Tags.get_tag(tag) #check if tag is in table
        if object:
            post_tags.append(object)
            object.count += 1
            object.save()
        else:
            t= Tags.objects.create(
                name = tag,
                count = 1
            )
            post_tags.append(t)
    return post_tags
