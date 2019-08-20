import pytest
from rest_framework import serializers

from imports.serializers import ImportCreateSerializer


@pytest.mark.django_db
def test_import_serializer():
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

    s = ImportCreateSerializer(data=test_case)
    assert s.is_valid(raise_exception=True)


wrong_relations_test_case_not_symmetrical = {
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
            "relatives": [2, 3]
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


wrong_relations_test_case_not_exists = {
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
            "relatives": [2, 3]
        },
    ]
}


@pytest.mark.parametrize('test_case', [
    wrong_relations_test_case_not_exists,
    wrong_relations_test_case_not_symmetrical
])
@pytest.mark.django_db
def test_import_serializer_should_raise_on_wrong_relations(test_case):
    s = ImportCreateSerializer(data=test_case)
    with pytest.raises(serializers.ValidationError):
        assert s.is_valid(raise_exception=True)
        assert s.save()
