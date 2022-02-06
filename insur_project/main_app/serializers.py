from rest_framework import serializers
from .models import Users, Licenses, Vehicles, Contracts, Payables
from counter.models import Mileages


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licenses
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = '__all__'


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contracts
        fields = '__all__'


class PayableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payables
        fields = '__all__'


class MileageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mileages
        fields = '__all__'
