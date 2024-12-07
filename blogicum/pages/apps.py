from django.apps import AppConfig


class PagesConfig(AppConfig):
    """Класс, отвечающий за настройку приложения pages."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
    verbose_name = 'Страница'
    verbose_name_plural = 'Страницы'
