from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое поста', blank=True, null=True)
    image = models.ImageField(upload_to='images/', verbose_name='Превью', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    publication = models.BooleanField(verbose_name='Признак публикации', )

    views_counter = models.PositiveIntegerField(verbose_name='Количество просмотров', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["title"]
