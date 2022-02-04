from django.apps import AppConfig


class CounterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'counter'

    def ready(self):
        from task_scheduler import run_scheduler
        run_scheduler.start()
