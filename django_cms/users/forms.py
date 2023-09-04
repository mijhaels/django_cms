from allauth.account.forms import SignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms import ChoiceField, DateField, DateInput, CharField
from django.contrib.auth.models import Group

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        error_messages = {
            "username": {"unique": "Este usuario ya existe"},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    name = CharField(label="Nombre completo", required=False)
    sex = ChoiceField(
        choices=(("", "Selecciona el sexo"), ("M", "Masculino"), ("F", "Femenino"), ("O", "Otro")),
        label="Sexo",
        required=False,
    )
    birth_date = DateField(label="Fecha de nacimiento", required=False, widget=DateInput(attrs={"type": "date"}))

    def save(self, request):
        user = super(UserSignupForm, self).save(request)
        # Asignar grupo
        group = Group.objects.get(name="Suscriptor")
        user.groups.add(group)
        # Asignar campos personalizados
        user.name = self.cleaned_data["name"]
        user.sex = self.cleaned_data["sex"]
        user.birth_date = self.cleaned_data["birth_date"]
        user.save()
        return user
