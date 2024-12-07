from django.db import models


class BlogAbstracModel(models.Model):
    """Абстрактная модель для моделей Blog."""

    is_published = models.BooleanField(
        verbose_name='Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField(verbose_name='Добавлено',
                                      auto_now_add=True)

    class Meta:
        """Класс метаданных."""

        abstract = True
