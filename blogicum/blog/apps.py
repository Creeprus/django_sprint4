from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Класс, отвечающий за настройку приложения blog."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Блог'
    verbose_name_plural = 'Блоги'
