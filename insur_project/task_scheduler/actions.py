from counter.models import Mileages


def generate_random_mileage():
    new_entry = Mileages()
    new_entry.date = '2030-01-01'
    new_entry.km = 88
    new_entry.contract_id = 'A921075001'
    new_entry.save()
    print("saving new entry")
