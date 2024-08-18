from django.db import models

class HebbModel(models.Model):
    weights = models.JSONField(default=list)  # Usando JSONField para armazenar a lista diretamente
    bias = models.FloatField(default=0.0)


