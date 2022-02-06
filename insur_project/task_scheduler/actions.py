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

    new_entry = []
    # create new entry for each active contract
    for i in range(len(active_contracts)):
        n = random.randint(0, 70000)
        n_decimal = Decimal(n) / Decimal(1000)

        new_entry.append({'data': yesterday, 'km': n_decimal, 'contract_no': active_contracts[i]['contract_no']})

    print(new_entry)
    # Create de-serializer to insert data
    class MileageSerializer(serializers.ModelSerializer):
        class Meta:
            model = Mileages
            field = '__all__'

    serializer = MileageSerializer(data=new_entry, many=True)
    # serializer = MileageSerializer(data=active_contracts, many=True)
    #
    if serializer.is_valid():
        print(serializer.validated_data)
        print("valid")

    # else:
    #     print(active_contracts)
    #     print(serializer)
    # new_entry = Mileages()
    # new_entry.date = '2030-01-01'
    # new_entry.km = 88
    # new_entry.contract_id = 'A921075001'
    # new_entry.save()
