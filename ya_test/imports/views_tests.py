import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from imports.models import Import, Citizen


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
