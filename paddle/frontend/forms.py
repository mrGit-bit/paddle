from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction

from games.models import Player

User = get_user_model()

EMAIL_WARNING_TEXT = (
    "Usa un correo electrónico al que tengas acceso. "
    "Lo necesitarás en caso de que tengas que recuperar tu contraseña."
)


def normalize_email_for_match(value):
    return (value or "").strip().lower()


class StyledFormMixin:
    def _mark_invalid_fields(self):
        for field_name in self.errors:
            field = self.fields.get(field_name)
            if not field:
                continue
            css_classes = field.widget.attrs.get("class", "")
            if "is-invalid" not in css_classes:
                field.widget.attrs["class"] = f"{css_classes} is-invalid".strip()


class RegistrationForm(StyledFormMixin, forms.Form):
    username = forms.CharField(
        min_length=3,
        max_length=15,
        label="Usuario*",
        error_messages={
            "required": "Este campo es obligatorio.",
            "min_length": "Nombre de usuario de 3 a 15 caracteres. Solo letras, números y @/./+/-/_.",
            "max_length": "Nombre de usuario de 3 a 15 caracteres. Solo letras, números y @/./+/-/_.",
        },
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "username",
                "autocomplete": "username",
                "autocapitalize": "off",
                "autocorrect": "off",
                "spellcheck": "false",
                "placeholder": "Tu nombre de usuario",
                "pattern": "^[a-zA-Z0-9@.+-_]{3,15}$",
                "maxlength": "15",
                "minlength": "3",
            }
        ),
    )
    email = forms.EmailField(
        label="Correo electrónico*",
        error_messages={
            "required": "Este campo es obligatorio.",
            "invalid": "Introduce un correo electrónico válido.",
        },
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "email",
                "autocomplete": "email",
                "autocapitalize": "off",
                "autocorrect": "off",
                "spellcheck": "false",
                "placeholder": "Correo electrónico",
                "data-confirm-target": "email",
                "data-confirm-normalize": "email",
            }
        ),
    )
    confirm_email = forms.EmailField(
        label="Confirma tu correo electrónico*",
        error_messages={
            "required": "Este campo es obligatorio.",
            "invalid": "Introduce un correo electrónico válido.",
        },
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "confirm_email",
                "autocomplete": "email",
                "autocapitalize": "off",
                "autocorrect": "off",
                "spellcheck": "false",
                "placeholder": "Confirma tu correo electrónico",
                "data-confirm-source": "email",
                "data-confirm-normalize": "email",
            }
        ),
    )
    password = forms.CharField(
        min_length=8,
        label="Contraseña*",
        error_messages={
            "required": "Este campo es obligatorio.",
            "min_length": "La contraseña debe tener al menos 8 caracteres.",
        },
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "password",
                "autocomplete": "new-password",
                "autocapitalize": "off",
                "autocorrect": "off",
                "spellcheck": "false",
                "placeholder": "Contraseña",
                "minlength": "8",
                "data-confirm-target": "password",
            }
        ),
    )
    confirm_password = forms.CharField(
        label="Confirma tu contraseña*",
        error_messages={
            "required": "Este campo es obligatorio.",
        },
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "confirm_password",
                "autocomplete": "new-password",
                "autocapitalize": "off",
                "autocorrect": "off",
                "spellcheck": "false",
                "placeholder": "Confirma tu contraseña",
                "data-confirm-source": "password",
            }
        ),
    )
    gender = forms.ChoiceField(
        choices=(
            ("", "Selecciona género"),
            (Player.GENDER_MALE, "Hombre"),
            (Player.GENDER_FEMALE, "Mujer"),
        ),
        label="Género*",
        error_messages={
            "required": "Por favor, selecciona tu género.",
            "invalid_choice": "Por favor, selecciona un género válido.",
        },
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "gender",
            }
        ),
    )
    player_id = forms.ModelChoiceField(
        queryset=Player.objects.none(),
        required=False,
        empty_label="No, soy un nuevo jugador",
        label="Te han anotado resultados? Qué jugador eres?",
        error_messages={
            "invalid_choice": "El jugador seleccionado ya no está disponible.",
        },
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "player_id",
            }
        ),
    )

    def __init__(self, *args, player_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["player_id"].queryset = (
            player_queryset if player_queryset is not None else Player.objects.none()
        )
        self._mark_invalid_fields()

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        user_exists = User.objects.filter(username__iexact=username).exists()
        selected_player = self.cleaned_data.get("player_id")
        player_exists = (
            Player.objects.filter(name__iexact=username, registered_user__isnull=True)
            .exclude(id=selected_player.id if selected_player else None)
            .exists()
        )
        if user_exists or player_exists:
            raise forms.ValidationError(
                (
                    "Ya existe un usuario o un jugador con ese nombre. "
                    "Cambia el nombre del usuario o selecciona el jugador existente."
                )
            )
        return username

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if normalize_email_for_match(email) != normalize_email_for_match(confirm_email):
            self.add_error("confirm_email", "Los correos electrónicos no coinciden.")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Las contraseñas no coinciden.")

        return cleaned_data

    @transaction.atomic
    def save(self):
        user = User(username=self.cleaned_data["username"], email=self.cleaned_data["email"].strip())
        user.set_password(self.cleaned_data["password"])
        user.save()

        selected_player = self.cleaned_data.get("player_id")
        if selected_player:
            selected_player.registered_user = user
            selected_player.name = user.username
            selected_player.gender = self.cleaned_data["gender"]
            selected_player.save()
        else:
            Player.objects.create(
                name=user.username,
                registered_user=user,
                gender=self.cleaned_data["gender"],
            )
        return user


class ProfileUpdateForm(StyledFormMixin, forms.Form):
    username = forms.CharField(
        min_length=3,
        max_length=15,
        label="Usuario*",
        error_messages={
            "required": "Este campo es obligatorio.",
            "min_length": "Nombre de usuario de 3 a 15 caracteres. Solo letras, números y @/./+/-/_.",
            "max_length": "Nombre de usuario de 3 a 15 caracteres. Solo letras, números y @/./+/-/_.",
        },
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "username",
                "autocomplete": "username",
                "autocapitalize": "off",
                "autocorrect": "off",
                "spellcheck": "false",
                "placeholder": "Tu nombre de usuario",
                "pattern": "^[a-zA-Z0-9@.+-_]{3,15}$",
                "maxlength": "15",
                "minlength": "3",
            }
        ),
    )
    email = forms.EmailField(
        label="Correo electrónico*",
        error_messages={
            "required": "Este campo es obligatorio.",
            "invalid": "Introduce un correo electrónico válido.",
        },
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "email",
                "autocomplete": "email",
                "autocapitalize": "off",
                "autocorrect": "off",
                "spellcheck": "false",
                "placeholder": "Correo electrónico",
            }
        ),
    )
    confirm_email = forms.EmailField(
        required=False,
        label="Confirma tu correo electrónico",
        error_messages={
            "invalid": "Introduce un correo electrónico válido.",
        },
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "confirm_email",
                "autocomplete": "email",
                "autocapitalize": "off",
                "autocorrect": "off",
                "spellcheck": "false",
                "placeholder": "Confirma tu correo electrónico",
            }
        ),
    )

    def __init__(self, *args, user, **kwargs):
        self.user = user
        self.linked_player = Player.objects.filter(registered_user=user).first()
        initial = kwargs.setdefault("initial", {})
        initial.setdefault("username", user.username)
        initial.setdefault("email", user.email)
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["data-original-email"] = user.email or ""
        self.show_confirm_email = self._email_change_requested()
        self._mark_invalid_fields()

    def _email_change_requested(self):
        if not self.is_bound:
            return False

        posted_email = self.data.get(self.add_prefix("email"))
        return normalize_email_for_match(posted_email) != normalize_email_for_match(self.user.email)

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()

        user_exists = User.objects.filter(username__iexact=username).exclude(pk=self.user.pk).exists()
        player_qs = Player.objects.filter(name__iexact=username)
        if self.linked_player:
            player_qs = player_qs.exclude(pk=self.linked_player.pk)
        if user_exists or player_qs.exists():
            raise forms.ValidationError(
                (
                    "Ya existe un usuario o un jugador con ese nombre. "
                    "Elige otro nombre de usuario."
                )
            )
        return username

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")

        if normalize_email_for_match(email) != normalize_email_for_match(self.user.email):
            self.show_confirm_email = True
            if not confirm_email:
                self.add_error(
                    "confirm_email",
                    "Confirma tu correo electrónico si quieres cambiarlo.",
                )
            elif normalize_email_for_match(email) != normalize_email_for_match(confirm_email):
                self.add_error("confirm_email", "Los correos electrónicos no coinciden.")

        return cleaned_data

    @transaction.atomic
    def save(self):
        new_username = self.cleaned_data["username"]
        new_email = (self.cleaned_data["email"] or "").strip()

        self.user.username = new_username
        self.user.email = new_email
        self.user.save()

        if self.linked_player and self.linked_player.name != new_username:
            self.linked_player.name = new_username
            self.linked_player.save(update_fields=["name"])

        return self.user
