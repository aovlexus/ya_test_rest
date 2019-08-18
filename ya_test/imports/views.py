from collections import OrderedDict

from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from imports.serializers import ImportCreateSerializer


class ImportViewSet(
    mixins.CreateModelMixin,
    GenericViewSet
):
    serializer_class = ImportCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            OrderedDict([
                ('data', serializer.data)
            ]),
            status=status.HTTP_201_CREATED,
            headers=headers
        )
