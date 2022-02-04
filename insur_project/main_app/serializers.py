from rest_framework import serializers
from .models import Users, Licenses, Vehicles


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
