from rest_framework import viewsets

from imports.serializers import ImportCreateSerializer


class ImportViewSet(viewsets.ModelViewSet):
    serializer_class = ImportCreateSerializer

