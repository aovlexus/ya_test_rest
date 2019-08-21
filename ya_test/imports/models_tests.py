import datetime
from typing import List

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
        CitizenRelations(from_citizen=citizens[0], to_citizen_id=citizens[0].citizen_id),
        CitizenRelations(from_citizen=citizens[0], to_citizen_id=citizens[1].citizen_id),
        CitizenRelations(from_citizen=citizens[1], to_citizen_id=citizens[0].citizen_id),
        CitizenRelations(from_citizen=citizens[0], to_citizen_id=citizens[2].citizen_id),
        CitizenRelations(from_citizen=citizens[2], to_citizen_id=citizens[0].citizen_id),
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


@pytest.mark.django_db
def test_import_get_birthdays():
    # citizens:
    # 0 - [0, 1, 2] april
    # 1 - [0] april
    # 2 - [2] august
    # 3 - [] september
    data_import = ImportFactory.create()
    citizens = [
        CitizenFactory.create(citizen_id=0, data_import_id=data_import.pk, birth_date=datetime.date(day=1, month=4, year=2000)),
        CitizenFactory.create(citizen_id=1, data_import_id=data_import.pk, birth_date=datetime.date(day=1, month=4, year=1994)),
        CitizenFactory.create(citizen_id=2, data_import_id=data_import.pk, birth_date=datetime.date(day=1, month=8, year=2000)),
        CitizenFactory.create(citizen_id=3, data_import_id=data_import.pk, birth_date=datetime.date(day=1, month=9, year=1990)),
    ]

    relations = [
        CitizenRelations(from_citizen=citizens[0], to_citizen_id=citizens[0].citizen_id),
        CitizenRelations(from_citizen=citizens[0], to_citizen_id=citizens[1].citizen_id),
        CitizenRelations(from_citizen=citizens[0], to_citizen_id=citizens[2].citizen_id),
        CitizenRelations(from_citizen=citizens[1], to_citizen_id=citizens[0].citizen_id),
        CitizenRelations(from_citizen=citizens[2], to_citizen_id=citizens[0].citizen_id),
    ]

    CitizenRelations.objects.bulk_create(relations)

    assert list(data_import.get_months_birthdays_stats().order_by(
        'month', 'to_citizen_id')
    ) == [
        {'birthdays': 2, 'month': 4, 'to_citizen_id': 0},
        {'birthdays': 1, 'month': 4, 'to_citizen_id': 1},
        {'birthdays': 1, 'month': 4, 'to_citizen_id': 2},
        {'birthdays': 1, 'month': 8, 'to_citizen_id': 0}
    ]


@pytest.mark.django_db
def test_citizen_remove_all_relatives_should_remove():
    data_import = ImportFactory.create()
    citizens: List[Citizen] = [
        CitizenFactory.create(citizen_id=0, data_import_id=data_import.pk, birth_date=datetime.date(day=1, month=4, year=2000)),
        CitizenFactory.create(citizen_id=1, data_import_id=data_import.pk, birth_date=datetime.date(day=1, month=4, year=1994)),
        CitizenFactory.create(citizen_id=2, data_import_id=data_import.pk, birth_date=datetime.date(day=1, month=8, year=2000)),
        CitizenFactory.create(citizen_id=3, data_import_id=data_import.pk, birth_date=datetime.date(day=1, month=9, year=1990)),
    ]

    relations = [
        CitizenRelations(from_citizen=citizens[0], to_citizen_id=citizens[0].citizen_id),
        CitizenRelations(from_citizen=citizens[0], to_citizen_id=citizens[1].citizen_id),
        CitizenRelations(from_citizen=citizens[0], to_citizen_id=citizens[2].citizen_id),
        CitizenRelations(from_citizen=citizens[1], to_citizen_id=citizens[0].citizen_id),
        CitizenRelations(from_citizen=citizens[2], to_citizen_id=citizens[0].citizen_id),
        CitizenRelations(from_citizen=citizens[3], to_citizen_id=citizens[2].citizen_id),
        CitizenRelations(from_citizen=citizens[2], to_citizen_id=citizens[3].citizen_id),
    ]

    CitizenRelations.objects.bulk_create(relations)

    citizens[0].remove_all_relatives()

    citizens_expected = Citizen.objects.all().order_by('id')
    assert citizens_expected[0].relatives == []
    assert citizens_expected[1].relatives == []
    assert citizens_expected[2].relatives == [3]
    assert citizens_expected[3].relatives == [2]
