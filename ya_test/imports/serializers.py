from collections import OrderedDict, defaultdict

from django.conf import settings
from rest_framework import serializers

from imports.models import Citizen, CitizenRelations, Import


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

    def validate_relations(self, relations):
        for citizen_id, relation in relations.items():
            for value in relation:
                try:
                    if citizen_id not in relations[value]:
                        raise serializers.ValidationError()
                except KeyError:
                    raise serializers.ValidationError()

    def create(self, validated_data):
        citizens_data = validated_data.pop('citizens')
        data_import = Import.objects.create(**validated_data)
        citizens = []
        relations = OrderedDict()

        for citizen_data in citizens_data:
            citizen_id = citizen_data['citizen_id']
            relations[citizen_id] = set(citizen_data.pop('relatives'))
            citizens.append(
                Citizen(
                    data_import_id=data_import.pk,
                    **citizen_data
                )
            )
        citizen_ids = Citizen.objects.bulk_create(citizens)

        #  TODO: Think how to validate on `is_valid()`
        self.validate_relations(relations)

        citizen_relations = []
        for relation, citizen_pk in zip(relations.values(), citizen_ids):
            for citizen_id in relation:
                citizen_relations.append(
                    CitizenRelations(
                        citizen_1=citizen_pk,
                        to_citizen_id=citizen_id
                    )
                )

        CitizenRelations.objects.bulk_create(citizen_relations)

        return data_import


class GiftsImportReadSerializer(serializers.Serializer):
    def to_representation(self, instance):
        instance = instance.get_months_birthdays_stats()
        result = defaultdict(list)
        for line in instance:
            result[line['month']].append(
                {
                    'citizen_id': line['to_citizen_id'],
                    'presents': line['birthdays']
                }
            )
        for month_number in range(1, 13):
            result[month_number] = result[month_number]
        return result

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError
