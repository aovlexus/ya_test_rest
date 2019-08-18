from django.conf import settings
from rest_framework import serializers

from imports.models import Import, Citizen


class CitizenSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(
        format=settings.DATE_FORMAT,
        input_formats=[settings.DATE_FORMAT]
    )

    # relatives = serializers.ListField(serializers.IntegerField())

    class Meta:
        model = Citizen
        fields = (
            'citizen_id',
            'town',
            'street',
            'building',
            'apartment',
            'birth_date',
            'gender',
            # 'relatives',
        )


class ImportCreateSerializer(serializers.ModelSerializer):
    citizens = CitizenSerializer(many=True)

    class Meta:
        model = Import
        fields = ('citizens', )

    def create(self, validated_data):
        citizens_data = validated_data.pop('citizens')
        data_import = Import.objects.create(**validated_data)
        citizens = [
            Citizen(
                data_import_id=data_import.pk,
                **citizen_data
            )
            for citizen_data in citizens_data
        ]
        Citizen.objects.bulk_create(citizens)
        return data_import
