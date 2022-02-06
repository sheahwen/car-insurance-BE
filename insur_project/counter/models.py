from django.db import models
from main_app.models import Contracts


class Mileages(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    km = models.DecimalField(max_digits=8, decimal_places=3)
    contract = models.ForeignKey(Contracts, on_delete=models.DO_NOTHING)

    def __str__(self):
        return 'KiLoMeTeR'
