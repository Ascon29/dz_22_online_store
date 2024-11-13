from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField

from catalog.models import Product


forbidden_words = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class StyleForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ProductForm(StyleForm, ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Ведите название"}
        )

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return price

    def clean_name(self):
        name = self.cleaned_data.get("name").lower()
        for word in forbidden_words:
            if word in name:
                raise ValidationError(f"{word} - запрещенное слово для названия")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description").lower()
        for word in forbidden_words:
            if word in description:
                raise ValidationError(f"{word} - запрещенное слово для описания")
        return description

    # def clean(self):
    #     cleaned_data = super().clean()
    #     name = cleaned_data.get("name").lower()
    #     description = cleaned_data.get("description").lower()
    #
    #     for word in forbidden_words:
    #         if word in name or word in description:
    #             raise ValidationError(
    #                 f"Нельзя добавить товар с словом {word} в описании или названии"
    #             )
    #     return cleaned_data
