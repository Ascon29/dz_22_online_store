from django.contrib.auth.forms import UserCreationForm

from catalog.forms import StyleForm
from users.models import User


class UserRegisterForm(StyleForm, UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "phone_number",
            "avatar",
            "country",
            "password1",
            "password2",
        )
