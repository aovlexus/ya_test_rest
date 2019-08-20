from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models

# Create your models here.
from django.db.models import Count, Q
from django.db.models.functions import ExtractMonth


class Import(models.Model):
    def get_months_birthdays_stats(self):
        #  Due to relations are symmetrical (the exists for both citizens)
        #  we can use "from_citizen"
        #  as gift receiver :) and to_citizen_id as giver
        qs = CitizenRelations.objects.filter(
            citizen_1__data_import_id=self.pk
        ).annotate(
            month=ExtractMonth('citizen_1__birth_date')
        ).values(
            'month', 'to_citizen_id'
        ).annotate(
            birthdays=Count('citizen_1_id')
        ).order_by('to_citizen_id')
        return qs

    def get_percentile(self):
        qs = CitizenRelations.objects.filter(
            citizen_1__data_import_id=self.pk
        ).annotate(
            month=ExtractMonth('citizen_1__birth_date')
        ).values(
            'month', 'to_citizen_id'
        ).annotate(
            birthdays=Count('citizen_1_id')
        ).order_by('to_citizen_id')
        return qs


class CitizenQuerySet(models.QuerySet):
    def with_relatives(self):
        clone = self._chain()
        clone = clone.annotate(
            relatives=ArrayAgg(
                'related_1__to_citizen_id',
                filter=Q(related_1__to_citizen_id__isnull=False)

            ),
        )
        return clone


class CitizenManager(models.Manager.from_queryset(CitizenQuerySet)):
    def get_queryset(self):
        #  order by id here because of deprecation Meta.ordering in Django 3.1
        #  https://docs.djangoproject.com/en/dev/internals/deprecation/#deprecation-removed-in-3-1
        return super().get_queryset().with_relatives().order_by('id')


class Citizen(models.Model):
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'

    objects = CitizenManager()

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
        unique_together = ('citizen_id', 'data_import')


class CitizenRelations(models.Model):
    citizen_1 = models.ForeignKey(
        Citizen,
        on_delete=models.DO_NOTHING,
        related_name='related_1'
    )

    to_citizen_id = models.IntegerField()
