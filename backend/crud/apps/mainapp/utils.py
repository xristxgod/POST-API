from typing import Dict

from django.contrib.contenttypes.models import ContentType


class ContentTypeError(Exception):
    pass


def get_content_value(obj_name: str, obj_id: int) -> Dict:
    if obj_name not in ['User', 'Post', 'Comment']:
        raise ContentTypeError()
    return {
        'content_type': ContentType.objects.get_by_natural_key('mainapp', obj_name),
        'object_id': obj_id
    }
