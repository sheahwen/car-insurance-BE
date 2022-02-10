import random
from decimal import Decimal
from datetime import date, timedelta

from rest_framework import serializers

from counter.models import Mileages
from main_app.models import Contracts


def generate_random_mileage():
    # retrieve all active contracts - application_status == true && between start and end dates
    yesterday = date.today()-timedelta(days=1)

    active_contracts = Contracts.objects.filter(
        application_status=True,
        start_date__lte=yesterday,
        end_date__gte=yesterday
    ).values('contract_no')

    # create new entry for each active contract
    for i in range(len(active_contracts)):
        n = random.randint(0, 70000)
        n_decimal = Decimal(n) / Decimal(1000)

        new_entry = Mileages(date=yesterday, km=n_decimal, contract_id=active_contracts[i]['contract_no'])
        new_entry.save()

    print("new mileage entries created")
