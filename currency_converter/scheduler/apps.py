"""Модуль с конфигом приложения scheduler."""

from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    """Конфиг класс для приложения анализатора."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self) -> None:
        """Метод для инидиализации периодических задач."""
        from scheduler.periodic_tasks import scheduler

        scheduler.start()
