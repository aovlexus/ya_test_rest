import datetime
from typing import List

import pytest
from django.conf import settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from imports.factories import ImportFactory, CitizenFactory
from imports.models import Import, Citizen, CitizenRelations


@pytest.mark.django_db
def test_imports_should_create_import():
    test_case = {
        "citizens": [
            {
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [2]
            },
            {
                "citizen_id": 2,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Сергей Иванович",
                "birth_date": "01.04.1997",
                "gender": "male",
                "relatives": [1]
            },
            {
                "citizen_id": 3,
                "town": "Керчь",
                "street": "Иосифа Бродского",
                "building": "2",
                "apartment": 11,
                "name": "Романова Мария Леонидовна",
                "birth_date": "23.11.1986",
                "gender": "female",
                "relatives": []
            },
        ]
    }

    client = APIClient()
    url = reverse('imports-list')

    r = client.post(url, data=test_case, format='json')

    assert r.status_code == status.HTTP_201_CREATED, r.json()
    assert Import.objects.all().count() == 1
    assert Citizen.objects.all().count() == 3
    import_id = Import.objects.all()[0]
    assert r.json() == {
        "data": {
            "import_id": import_id.pk
        }
    }


@pytest.mark.django_db
def test_imports_should_create_correct_relations():
    test_case = {
        "citizens": [
            {
                "citizen_id": 100,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [200, 300]
            },
            {
                "citizen_id": 200,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Сергей Иванович",
                "birth_date": "01.04.1997",
                "gender": "male",
                "relatives": [100]
            },
            {
                "citizen_id": 300,
                "town": "Керчь",
                "street": "Иосифа Бродского",
                "building": "2",
                "apartment": 11,
                "name": "Романова Мария Леонидовна",
                "birth_date": "23.11.1986",
                "gender": "female",
                "relatives": [100]
            },
        ]
    }

    client = APIClient()
    url = reverse('imports-list')

    r = client.post(url, data=test_case, format='json')

    import_id = r.json()["data"]["import_id"]
    assert set(
        Citizen.objects.get(data_import_id=import_id, citizen_id=100).relatives
    ) == {200, 300}

    assert set(
        Citizen.objects.get(data_import_id=import_id, citizen_id=200).relatives
    ) == {100}

    assert set(
        Citizen.objects.get(data_import_id=import_id, citizen_id=300).relatives
    ) == {100}


@pytest.mark.django_db
def test_should_get_citizen():
    i = ImportFactory.create()
    citizens: List[Citizen] = [
        CitizenFactory.create(data_import_id=i.pk),
        CitizenFactory.create(data_import_id=i.pk)
    ]
    relations = [
        CitizenRelations(citizen_1=citizens[0], to_citizen_id=citizens[1].citizen_id),
        CitizenRelations(citizen_1=citizens[1], to_citizen_id=citizens[0].citizen_id),
    ]
    CitizenRelations.objects.bulk_create(relations)

    citizens = Citizen.objects.filter(id__in=[citizens[0].pk, citizens[1].pk])

    client = APIClient()
    url = reverse('imports-citizens', kwargs={'pk': i.pk})

    r = client.get(url, format='json')

    assert r.status_code == status.HTTP_200_OK, r.json()
    assert r.json() == {
        "data": [
            {
                "citizen_id": citizens[0].citizen_id,
                "town": citizens[0].town,
                "street": citizens[0].street,
                "building": citizens[0].building,
                "apartment": citizens[0].apartment,
                "name": citizens[0].name,
                "birth_date": citizens[0].birth_date.strftime(settings.DATE_FORMAT),
                "gender": citizens[0].gender,
                "relatives": [citizens[1].citizen_id]
            },
            {
                "citizen_id": citizens[1].citizen_id,
                "town": citizens[1].town,
                "street": citizens[1].street,
                "building": citizens[1].building,
                "apartment": citizens[1].apartment,
                "name": citizens[1].name,
                "birth_date": citizens[1].birth_date.strftime(settings.DATE_FORMAT),
                "gender": citizens[1].gender,
                "relatives": [citizens[0].citizen_id]
            },
        ]
    }


@pytest.mark.django_db
def test_birthdays_should_return_correct_data():
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
        CitizenRelations(citizen_1=citizens[0], to_citizen_id=citizens[0].citizen_id),
        CitizenRelations(citizen_1=citizens[0], to_citizen_id=citizens[1].citizen_id),
        CitizenRelations(citizen_1=citizens[0], to_citizen_id=citizens[2].citizen_id),
        CitizenRelations(citizen_1=citizens[1], to_citizen_id=citizens[0].citizen_id),
        CitizenRelations(citizen_1=citizens[2], to_citizen_id=citizens[0].citizen_id),
    ]
    CitizenRelations.objects.bulk_create(relations)

    client = APIClient()
    url = reverse('imports-citizens-birthdays', kwargs={'pk': data_import.pk})

    r = client.get(url, format='json')

    assert r.status_code == status.HTTP_200_OK
    assert r.json() == {
        "data": {
            "1": [],
            "2": [],
            "3": [],
            "4": [
                {
                    "citizen_id": citizens[0].citizen_id,
                    "presents": 2
                },
                {
                    "citizen_id": citizens[1].citizen_id,
                    "presents": 1
                },
                {
                    "citizen_id": citizens[2].citizen_id,
                    "presents": 1
                },
            ],
            "5": [],
            "6": [],
            "7": [],
            "8": [
                {
                    "citizen_id": citizens[0].citizen_id,
                    "presents": 1
                },
            ],
            "9": [],
            "10": [],
            "11": [],
            "12": [],
        }
    }


@pytest.mark.django_db
def test_imports_should_patch_citizen():
    data_import = ImportFactory()
    CitizenFactory(
        citizen_id=1, town="Москва", street="Льва Толстого",
        building="16к7стр5", apartment=7, name="Иванов Иван Иванович",
        birth_date=datetime.date(1994, 1, 1), gender="male",
        data_import_id=data_import.pk
    )
    CitizenFactory(
        citizen_id=2, town="Москва", street="Льва Толстого",
        building="16к7стр7", apartment=7, name="Иванов Сергей Иванович",
        birth_date=datetime.date(1980, 2, 2), gender="female",
        data_import_id=data_import.pk

    )

    client = APIClient()
    url = reverse('imports-citizen-update', kwargs={
        'pk': data_import.pk, 'citizen_id': 1
    })

    r = client.patch(
        url,
        data={
            "town": "Санкт-Петербург"
        },
        format='json'
    )

    assert r.status_code == status.HTTP_200_OK, r.json()
    assert r.json() == {
        "data": {
            "citizen_id": 1,
            "town": "Санкт-Петербург",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Иван Иванович",
            "birth_date": "01.01.1994",
            "gender": "male",
            "relatives": []
        }
    }


@pytest.mark.django_db
def test_imports_should_patch_citizen_relatives():
    data_import = ImportFactory()
    citizens = [
        CitizenFactory(
            citizen_id=1, town="Москва", street="Льва Толстого",
            building="16к7стр5", apartment=7, name="Иванов Иван Иванович",
            birth_date=datetime.date(1994, 1, 1), gender="male",
            data_import_id=data_import.pk
        ),
        CitizenFactory(
            citizen_id=200, town="Москва", street="Льва Толстого",
            building="16к7стр7", apartment=7, name="Иванов Сергей Иванович",
            birth_date=datetime.date(1980, 2, 2), gender="female",
            data_import_id=data_import.pk

        )
    ]

    client = APIClient()
    url = reverse('imports-citizen-update', kwargs={
        'pk': data_import.pk, 'citizen_id': 1
    })

    r = client.patch(
        url,
        data={
            "town": "Санкт-Петербург",
            "relatives": [200]
        },
        format='json'
    )

    assert r.status_code == status.HTTP_200_OK, r.json()

    citizens[1] = Citizen.objects.filter(pk=citizens[1].pk)[0]
    assert citizens[1].relatives == [1]

    assert r.json() == {
        "data": {
            "citizen_id": 1,
            "town": "Санкт-Петербург",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Иван Иванович",
            "birth_date": "01.01.1994",
            "gender": "male",
            "relatives": [200]
        }
    }


@pytest.mark.django_db
def test_imports_should_return_400_on_wrong_relative():
    data_import = ImportFactory()
    CitizenFactory(
        citizen_id=1, town="Москва", street="Льва Толстого",
        building="16к7стр5", apartment=7, name="Иванов Иван Иванович",
        birth_date=datetime.date(1994, 1, 1), gender="male",
        data_import_id=data_import.pk
    )
    CitizenFactory(
        citizen_id=2, town="Москва", street="Льва Толстого",
        building="16к7стр7", apartment=7, name="Иванов Сергей Иванович",
        birth_date=datetime.date(1980, 2, 2), gender="female",
        data_import_id=data_import.pk

    )

    client = APIClient()
    url = reverse('imports-citizen-update', kwargs={
        'pk': data_import.pk, 'citizen_id': 1
    })

    r = client.patch(
        url,
        data={
            "town": "Санкт-Петербург",
            "relatives": [4]
        },
        format='json'
    )

    assert r.status_code == status.HTTP_400_BAD_REQUEST, r.json()
