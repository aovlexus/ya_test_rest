from typing import Optional, List

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

    @factory.post_generation
    def relatives(
        self,
        create: bool,
        extrcted: Optional[List[int]],
        **kwargs
    ) -> None:

        if not create:
            return

        if extrcted:
            self.relatives = extrcted
            relations = [
                models.CitizenRelations(
                    from_citizen_id=self.pk,
                    to_citizen_id=relative
                )
                for relative in extrcted
            ]
            models.CitizenRelations.objects.bulk_create(relations)


    class Meta:
        model = models.Citizen


class ImportFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Import
