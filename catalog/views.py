from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from catalog.forms import ProductForm
from catalog.models import Product, Category
from catalog.services import get_product_list_form_cache, get_product_category


class CategoryListView(ListView):
    model = Category


class CategoryProductView(ListView):
    template_name = "catalog/category_product.html"
    context_object_name = "category_product"

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return get_product_category(pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["category_product"] = self.get_queryset()
        return context


class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if not request.user.has_perm("catalog.can_unpublish_product"):
            return HttpResponseForbidden("У вас нет на это прав")

        product.publication_status = False
        product.save()
        return redirect("catalog:product_list")


class ContactsView(TemplateView):
    template_name = "catalog/contacts.html"


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        return get_product_list_form_cache()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["publicated_products"] = Product.objects.filter(publication_status=True)
    #     return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product_list")

    def get_form_class(self):
        user = self.request.user
        if user != self.object.owner:
            raise PermissionDenied
        return ProductForm

    # def post(self, request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     if self.request.user != product.owner:
    #         return HttpResponseForbidden('У вас нет на это прав')
    #     product.publication_status = False
    #     product.save()
    #     return redirect('catalog:product_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product_list")

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if (
            not self.request.user.has_perm("delete_product")
            and self.request.user != product.owner
        ):
            return HttpResponseForbidden("У вас нет на это прав")
        product.delete()
        return redirect("catalog:product_list")


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}, сообщение отправлено.")
    return render(request, "contacts.html")
