from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование категории")
    description = models.TextField(
        verbose_name="Описание товара", blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


def validate_file_size(value):
    """Функция для валидации размера файла"""
    filesize = value.size

    if filesize > 5242880:
        raise ValidationError("Максимальный размер файла не должен превышать 5MB")
    else:
        return value


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование товара")
    description = models.TextField(
        verbose_name="Описание товара", blank=True, null=True
    )
    image = models.ImageField(
        upload_to="images/",
        verbose_name="Изображение товара",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                ["jpg", "jpeg", "png"],
                message="Формат файла должен быть jpg, jpeg или png",
            ),
            validate_file_size,
        ],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="products",
    )
    price = models.FloatField(verbose_name="Цена товара")
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(auto_now=True, verbose_name="Дата изменения")

    publication_status = models.BooleanField(
        default=False, verbose_name="Статус публикации"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="products",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name}, цена: {self.price}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
        ]
