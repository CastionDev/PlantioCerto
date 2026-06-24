from django.db import models


class Cultura(models.Model):
    TIPOS = [
        ('hortaliça', 'Hortaliça'),
        ('fruto', 'Fruto'),
        ('raiz', 'Raiz'),
        ('legume', 'Legume'),
        ('cereal', 'Cereal'),
    ]

    nome_comum      = models.CharField(max_length=100)
    nome_cientifico = models.CharField(max_length=150, blank=True)
    dias_colheita   = models.PositiveIntegerField()
    tipo            = models.CharField(max_length=50, choices=TIPOS)

    def __str__(self):
        return self.nome_comum


class ExigenciaClimatica(models.Model):
    cultura         = models.OneToOneField(Cultura, on_delete=models.CASCADE, related_name='exigencia_climatica')
    temp_minima     = models.DecimalField(max_digits=5, decimal_places=2)
    temp_maxima     = models.DecimalField(max_digits=5, decimal_places=2)
    umidade_minima  = models.PositiveSmallIntegerField()
    umidade_maxima  = models.PositiveSmallIntegerField()
    chuva_minima_mm = models.DecimalField(max_digits=6, decimal_places=2)
    chuva_maxima_mm = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.cultura} – {self.temp_minima}°C a {self.temp_maxima}°C"


class FaseLunarIdeal(models.Model):
    FASES = [
        ('nova', 'Nova'),
        ('crescente', 'Crescente'),
        ('cheia', 'Cheia'),
        ('minguante', 'Minguante'),
    ]

    cultura  = models.ForeignKey(Cultura, on_delete=models.CASCADE, related_name='fases_lunares')
    fase_lua = models.CharField(max_length=20, choices=FASES)

    def __str__(self):
        return f"{self.cultura} – {self.fase_lua}"


class CalendarioPlantio(models.Model):
    REGIOES = [
        ('norte', 'Norte'),
        ('nordeste', 'Nordeste'),
        ('centro-oeste', 'Centro-Oeste'),
        ('sudeste', 'Sudeste'),
        ('sul', 'Sul'),
    ]

    cultura    = models.ForeignKey(Cultura, on_delete=models.CASCADE, related_name='calendarios')
    regiao     = models.CharField(max_length=50, choices=REGIOES)
    mes_inicio = models.PositiveSmallIntegerField()
    mes_fim    = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.cultura} – {self.regiao} ({self.mes_inicio} a {self.mes_fim})"