"""Модуль с конфигом приложения scheduler."""
import sys

from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    """Конфиг класс для приложения анализатора."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self) -> None:
        """Метод для инидиализации периодических задач."""
        if 'runserver' not in sys.argv and 'migrate' not in sys.argv and 'createsuperuser' not in sys.argv:

            from scheduler.periodic_tasks import scheduler

            scheduler.start()
