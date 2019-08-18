import pytest

from imports.factories import CitizenFactory, ImportFactory
from imports.models import Citizen, CitizenRelations


@pytest.mark.django_db
def test_citizen_get_with_relatives():
    data_import = ImportFactory.create()
    citizens = [
        CitizenFactory.create(data_import_id=data_import.pk),
        CitizenFactory.create(data_import_id=data_import.pk),
        CitizenFactory.create(data_import_id=data_import.pk),
        CitizenFactory.create(data_import_id=data_import.pk),
    ]

    relations = [
        CitizenRelations(citizen_1=citizens[0], to_citizen_id=citizens[0].citizen_id),
        CitizenRelations(citizen_1=citizens[0], to_citizen_id=citizens[1].citizen_id),
        CitizenRelations(citizen_1=citizens[1], to_citizen_id=citizens[0].citizen_id),
        CitizenRelations(citizen_1=citizens[0], to_citizen_id=citizens[2].citizen_id),
        CitizenRelations(citizen_1=citizens[2], to_citizen_id=citizens[0].citizen_id),
    ]

    CitizenRelations.objects.bulk_create(relations)

    citizens = Citizen.objects.all().order_by('id')

    assert set(citizens[0].relatives) == {
        citizens[0].citizen_id,
        citizens[1].citizen_id,
        citizens[2].citizen_id
    }
    assert citizens[1].relatives == [citizens[0].citizen_id]
    assert citizens[2].relatives == [citizens[0].citizen_id]
    assert citizens[3].relatives == []
