from django.db import models
from django.db.models import Func, Sum
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, LicenseSerializer, VehicleSerializer, ContractSerializer, PayableSerializer, \
    MileageSerializer
from .models import Users, Licenses, Vehicles, Contracts, Payables
from counter.models import Mileages
from datetime import date, timedelta
from decimal import *
import random


# function to extract month, year
class Month(Func):
    function = 'EXTRACT'
    template = '%(function)s(MONTH FROM %(expressions)s)'
    _output_field = models.IntegerField()


class Year(Func):
    function = 'EXTRACT'
    template = '%(function)s(YEAR FROM %(expressions)s)'
    _output_field = models.IntegerField()


class ViewAll(APIView):

    def get(self, request):
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)

        return Response(serializer.data)


class UserDetail(APIView):

    def get(self, request, pk):
        # generate basic user info
        e = Users.objects.prefetch_related('vehicles_set').select_related('licenses').get(id=pk)
        users = e
        vehicles = e.vehicles_set
        licenses = e.licenses
        serializer_user = UserSerializer(users)
        serializer_license = LicenseSerializer(licenses)
        serializer_vehicle = VehicleSerializer(vehicles, many=True)

        # generate contract details
        vehicle_numbers = [vehicle['vehicle_no'] for vehicle in serializer_vehicle.data]
        contracts = Contracts.objects.filter(vehicle_id__in=vehicle_numbers)
        serializer_contract = ContractSerializer(contracts, many=True)

        contract_numbers = [contract['contract_no'] for contract in serializer_contract.data]
        payables = Payables.objects.filter(contract_id__in=contract_numbers)
        mileages = Mileages.objects.filter(contract_id__in=contract_numbers)
        serializer_payable = PayableSerializer(payables, many=True)
        serializer_mileage = MileageSerializer(mileages, many=True)

        # aggregate past 12 months
        today = date.today()
        start_date = today - timedelta(days=365)
        aggregate_start_date = date(start_date.year, start_date.month, 1)

        month = (
            Mileages.objects.filter(contract_id__in=contract_numbers, date__gte=aggregate_start_date, date__lte=today)
            .annotate(month=Month('date'))
            .values('month')
            .annotate(total=Sum('km'))
            .annotate(year=Year('date'))
            .order_by('month'))

        # compile in an object
        data = {
            'user': serializer_user.data,
            'license': serializer_license.data,
            'vehicle': serializer_vehicle.data,
            'contract': serializer_contract.data,
            'payables': serializer_payable.data,
            'month': month,
            'mileage': serializer_mileage.data,
        }

        return Response(data)


class ChartDay(APIView):

    def get(self, request, pk):

        vehicles = Users.objects.filter(id=pk).values('vehicles__vehicle_no')
        vehicle_numbers = [vehicle['vehicles__vehicle_no'] for vehicle in vehicles]
        contracts = Contracts.objects.filter(vehicle_id__in=vehicle_numbers).values('contract_no')
        contract_numbers = [contract['contract_no'] for contract in contracts]

        # aggregate past 30 days
        today = date.today()
        yesterday = today - timedelta(days=1)
        start_date = today - timedelta(days=31)

        day = (
            Mileages.objects.filter(contract_id__in=contract_numbers, date__gte=start_date, date__lte=yesterday)
            .values('date')
            .annotate(total=Sum('km'))
            .order_by('date'))

        return Response(day)


class VehicleDetail(APIView):

    def get(self, request, pk):
        vehicle = Vehicles.objects.get(vehicle_no=pk)
        serializer_vehicle = VehicleSerializer(vehicle)
        contracts = Contracts.objects.get(vehicle_id=pk)
        serializer_contract = ContractSerializer(contracts)
        contract_number = serializer_contract.data['contract_no']
        mileage = Mileages.objects.filter(contract_id=contract_number).values('date', 'km')
        data = {'vehicle': serializer_vehicle.data, 'contract': serializer_contract.data, 'mileage': mileage}

        return Response(data)


class CreateUser(APIView):

    def post(self, request):

        newuser = Users(
            username=request.data['username'],
            password=request.data['password'],
            email=request.data['email']
        )

        newuser.save()

        license = Licenses(
            ic_no=request.data['ic'],
            first_name=request.data['firstname'],
            last_name=request.data['lastname'],
            phone=request.data['phone'],
            dob=request.data['dob'],
            license_no=request.data['licenseno'],
            expiry_date='2055-12-31',
            user=newuser
        )
        license.save()

        vehicle = Vehicles(
            vehicle_no=request.data['vehicleno'],
            vehicle_type=request.data['type'],
            make=request.data['make'],
            model=request.data['model'],
            capacity=request.data['capacity'],
            year_of_registration=request.data['registrationyear'],
            coe_expiry_date=request.data['coeexp'],
            user=newuser
        )
        vehicle.save()

        return Response("user created!")


class ActiveContracts(APIView):

    def get(self, request):
        yesterday = date.today() - timedelta(days=1)

        active_contracts = Contracts.objects.filter(
            application_status=True,
            start_date__lte=yesterday,
            end_date__gte=yesterday
        ).values('contract_no')

        for i in range(len(active_contracts)):
            n = random.randint(0, 70000)
            n_decimal = Decimal(n) / Decimal(1000)

            active_contracts[i]['date'] = yesterday
            active_contracts[i]['km'] = n_decimal

        return Response(active_contracts)
