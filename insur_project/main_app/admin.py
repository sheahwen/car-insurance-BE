from django.contrib import admin
from . import models
from datetime import date, timedelta, datetime

@admin.register(models.Contracts)
class ContractsAdmin(admin.ModelAdmin):
    list_display = ['contract_no', 'application_date', 'application_status']


@admin.register(models.Payables)
class PayablesAdmin(admin.ModelAdmin):
    list_display = ['contract_id', 'billing_month', 'due_date', 'amount']

    def billing_month(self, payables):
        datetime_obj = datetime.strptime(str(payables.month), '%m')
        month_name = datetime_obj.strftime("%b")
        return f'{month_name}-{payables.year}'


    def due_date(self, payables):
        due_date = date(payables.year, payables.month+3, 1)-timedelta(days=1)
        print(due_date)
        return due_date
