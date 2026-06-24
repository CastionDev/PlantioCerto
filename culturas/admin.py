from django.contrib import admin
from .models import Cultura, ExigenciaClimatica, FaseLunarIdeal, CalendarioPlantio


class ExigenciaClimaticaInline(admin.StackedInline):
    model = ExigenciaClimatica
    extra = 1


class FaseLunarInline(admin.TabularInline):
    model = FaseLunarIdeal
    extra = 1


class CalendarioInline(admin.TabularInline):
    model = CalendarioPlantio
    extra = 1


@admin.register(Cultura)
class CulturaAdmin(admin.ModelAdmin):
    list_display  = ('nome_comum', 'nome_cientifico', 'tipo', 'dias_colheita')
    list_filter   = ('tipo',)
    search_fields = ('nome_comum', 'nome_cientifico')
    inlines       = [ExigenciaClimaticaInline, FaseLunarInline, CalendarioInline]