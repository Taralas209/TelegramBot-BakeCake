from django.db import models
from .utils import shorten_link

class ShortenedLink(models.Model):
    original_link = models.URLField(verbose_name='Оригинальная ссылка')
    shortened_link = models.URLField(verbose_name='Сокращенная ссылка', blank=True)
    link_title = models.CharField(max_length=200, verbose_name='Название ссылки', blank=True)
    click_count = models.PositiveIntegerField(verbose_name='Количество кликов', default=0, editable=False)

    class Meta:
        verbose_name = 'Сокращенная ссылка'
        verbose_name_plural = 'Сокращенные ссылки'

    def save(self, *args, **kwargs):
        self.shortened_link = shorten_link(self.original_link, self.link_title)
        super().save(*args, **kwargs)
