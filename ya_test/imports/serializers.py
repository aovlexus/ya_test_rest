from django.conf import settings
from rest_framework import serializers

from imports.models import Import, Citizen, CitizenRelations


class BaseCitizenSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(
        format=settings.DATE_FORMAT,
        input_formats=[settings.DATE_FORMAT]
    )

    class Meta:
        model = Citizen
        fields = (
            'citizen_id',
            'town',
            'name',
            'street',
            'building',
            'apartment',
            'birth_date',
            'gender',
            'relatives',
        )


class ReadCitizenSerializer(BaseCitizenSerializer):
    relatives = serializers.ListField(serializers.IntegerField())


class CreateCitizenSerializer(BaseCitizenSerializer):
    relatives = serializers.ListField(
        write_only=True,
    )


class ImportCreateSerializer(serializers.ModelSerializer):
    citizens = CreateCitizenSerializer(many=True, write_only=True)
    import_id = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = Import
        fields = ('citizens', 'import_id', )

    def create(self, validated_data):
        citizens_data = validated_data.pop('citizens')
        data_import = Import.objects.create(**validated_data)
        citizens = []
        relations = []

        for citizen_data in citizens_data:
            relations.append(citizen_data.pop('relatives'))
            citizens.append(
                Citizen(
                    data_import_id=data_import.pk,
                    **citizen_data
                )
            )
        citizen_ids = Citizen.objects.bulk_create(citizens)

        citizen_relations = []
        for relation, citizen_pk in zip(relations, citizen_ids):
            for citizen_id in relation:
                citizen_relations.append(
                    CitizenRelations(
                        citizen_1=citizen_pk,
                        to_citizen_id=citizen_id
                    )
                )

        CitizenRelations.objects.bulk_create(citizen_relations)

        return data_import
