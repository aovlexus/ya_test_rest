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
    citizen_id = models.PositiveIntegerField()
    town = models.CharField(max_length=512)
    street = models.CharField(max_length=512)
    building = models.CharField(max_length=512)
    apartment = models.PositiveIntegerField()
    birth_date = models.DateField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    relatives = models.ManyToManyField(
        'self',
        symmetrical=True,
    )
