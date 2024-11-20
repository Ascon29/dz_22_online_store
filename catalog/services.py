from django.core.cache import cache

from catalog.models import Product, Category
from config.settings import CACHE_ENABLED


def get_product_list_form_cache():
    if not CACHE_ENABLED:
        return Product.objects.filter(publication_status=True)
    key = "product_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.filter(publication_status=True)
    cache.set(key, products, 60)
    return products


def get_product_category(pk):
    category = Category.objects.get(pk=pk)
    products = Product.objects.filter(category=category)
    return products
