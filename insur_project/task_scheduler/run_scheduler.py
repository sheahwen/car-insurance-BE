from apscheduler.schedulers.background import BackgroundScheduler
from task_scheduler import actions


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(actions.generate_random_mileage, 'cron', hour=10, minute=40, second=0)
    # scheduler.add_job(actions.generate_random_mileage, 'interval', seconds=10)
    scheduler.start()
