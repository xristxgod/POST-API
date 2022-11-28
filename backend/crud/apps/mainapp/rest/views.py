from rest_framework.generics import GenericAPIView
from rest_framework.serializers import ListSerializer

from drf_spectacular.utils import extend_schema

from apps.core.authentication import ApiTokenAuthentication


class Posts(GenericAPIView):
    authentication_classes = (ApiTokenAuthentication,)

    @extend_schema(
        request=None,
        responses={200: ListSerializer(child=NotImplementedError)},
        summary='Посты',
        description='Посты',
    )
    def get(self, request, *args, **kwargs):
        pass
