import factory
import factory.fuzzy

from imports import models


class CitizenFactory(factory.DjangoModelFactory):
    citizen_id = factory.Sequence(lambda n: n)
    town = factory.Faker('city')
    street = factory.Faker('street_name')
    building = factory.Faker('building_number')
    apartment = factory.Faker('building_number')
    birth_date = factory.Faker('date_object')
    gender = factory.fuzzy.FuzzyChoice(choices=('male', 'female'))
    name = factory.Faker('name')

    class Meta:
        model = models.Citizen


class ImportFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Import
