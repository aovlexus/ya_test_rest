from django.db import models

# Create your models here.


class Import(models.Model):
    pass


class Citizen(models.Model):
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'

    GENDER_CHOICES = (
        (GENDER_MALE, 'male'),
        (GENDER_FEMALE, 'female')
    )
    data_import = models.ForeignKey(
        Import,
        related_name='citizens',
        on_delete=models.DO_NOTHING
    )
    name = models.CharField(max_length=512)
    citizen_id = models.PositiveIntegerField()
    town = models.CharField(max_length=512)
    street = models.CharField(max_length=512)
    building = models.CharField(max_length=512)
    apartment = models.PositiveIntegerField()
    birth_date = models.DateField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    class Meta:
        ordering = ('id', )
        unique_together = ('citizen_id', 'data_import')


class CitizenRelations(models.Model):
    citizen_1 = models.ForeignKey(
        Citizen,
        on_delete=models.DO_NOTHING,
        related_name='related_1'
    )
    citizen_2 = models.ForeignKey(
        Citizen,
        on_delete=models.DO_NOTHING,
        related_name='related_2'
    )
