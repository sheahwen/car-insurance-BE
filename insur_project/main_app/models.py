from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from django.db import models
from django.db.models import Func, Sum
from datetime import date


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.username


class Licenses(models.Model):
    ic_no = models.CharField(max_length=9, primary_key=True, validators=[RegexValidator(regex=r'^[A-Z]\d{7}[A-Z]')])
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, unique=True)
    dob = models.DateField()
    license_no = models.CharField(max_length=9, unique=True, validators=[RegexValidator(regex=r'^[A-Z]\d{7}[A-Z]')])
    expiry_date = models.DateField()
    user = models.OneToOneField(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.ic_no


class Vehicles(models.Model):

    today_date = date.today()
    today_year = today_date.year

    vehicle_no = models.CharField(max_length=9, primary_key=True)
    vehicle_type = models.CharField(max_length=4)
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    capacity = models.PositiveSmallIntegerField()
    year_of_registration = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(today_year)])
    # may need to check today_year data type
    coe_expiry_date = models.DateField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.vehicle_no


class Contracts(models.Model):
    contract_no = models.CharField(max_length=10, primary_key=True, validators=[RegexValidator(regex=r'^[A-Z]\d{9}')])
    base_rate = models.PositiveIntegerField()
    km_rate = models.DecimalField(max_digits=3, decimal_places=2)
    start_date = models.DateField(null=True)  # same as approval date
    end_date = models.DateField(null=True)
    application_date = models.DateField(auto_now_add=True)
    application_status = models.BooleanField(default=False)
    vehicle = models.OneToOneField(Vehicles, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.contract_no

    class Meta:
        ordering = ['application_date']


class Payables(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    outstanding = models.BooleanField(default=True)
    contract = models.ForeignKey(Contracts, on_delete=models.PROTECT)
