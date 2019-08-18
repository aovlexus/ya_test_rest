from collections import OrderedDict

from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from imports.models import Citizen, Import
from imports.serializers import ImportCreateSerializer, CitizenSerializer


class ImportViewSet(
    mixins.CreateModelMixin,
    GenericViewSet
):
    serializer_class = ImportCreateSerializer
    queryset = Import.objects.all()

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

    @action(['get'], detail=True)
    def citizens(self, request, *args, pk=None):
        data_import = self.get_object()
        citizens = Citizen.objects.filter(data_import_id=data_import.pk)
        serializer = CitizenSerializer(instance=citizens, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(
            OrderedDict([
                ('data', serializer.data)
            ]),
            headers=headers
        )
