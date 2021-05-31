from django.contrib import admin
from . import models
from import_export.admin import ImportExportModelAdmin

class BorderStatusInline(admin.TabularInline):
    model = models.BorderStatus
    autocomplete_fields = ("destination",)
    extra = 0


@admin.register(models.OriginCountry)
class OriginCountryAdmin(ImportExportModelAdmin):
    inlines = [BorderStatusInline]
    search_fields = ('name',)
    autocomplete_fields = ("origin_country",)


@admin.register(models.Country)
class CountryAdmin(ImportExportModelAdmin):
    search_fields = ("name",)
    ordering = ("name",)

