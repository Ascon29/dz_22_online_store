from django.contrib import admin
from blog.models import Post


@admin.register(Post)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "content", "image", "created_at", "publication")
    list_filter = ("publication",)
    search_fields = (
        "title",
        "content",
    )
