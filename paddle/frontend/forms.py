from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.functions import Lower

from games.models import Group, Player

User = get_user_model()

EMAIL_WARNING_TEXT = (
    "Usa un correo electrónico al que tengas acceso. "
    "Lo necesitarás en caso de que tengas que recuperar tu contraseña."
)


def normalize_email_for_match(value):
    return (value or "").strip().lower()


def validate_unique_email(email, *, exclude_user=None):
    normalized_email = normalize_email_for_match(email)
    if not normalized_email:
        return email

    existing_users = User.objects.filter(email__iexact=normalized_email)
    if exclude_user is not None:
        existing_users = existing_users.exclude(pk=exclude_user.pk)

    if existing_users.exists():
        raise forms.ValidationError("Ya existe una cuenta con ese correo electrónico.")

    return (email or "").strip()


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
    GROUP_MODE_JOIN = "join"
    GROUP_MODE_CREATE = "create"
    GROUP_CHOICE_CREATE = "__create__"

    group_mode = forms.ChoiceField(
        choices=(
            (GROUP_MODE_JOIN, "Unirme a un grupo existente"),
            (GROUP_MODE_CREATE, "Crear un grupo nuevo"),
        ),
        initial=GROUP_MODE_JOIN,
        label="Grupo*",
        required=False,
        widget=forms.HiddenInput(),
    )
    group_choice = forms.ChoiceField(
        choices=(),
        required=False,
        label="Grupo/club*",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "group_choice",
            }
        ),
    )
    group_id = forms.ModelChoiceField(
        queryset=Group.objects.none(),
        required=False,
        empty_label="Selecciona grupo",
        label="Grupo existente",
        widget=forms.HiddenInput(),
    )
    new_group_name = forms.CharField(
        required=False,
        label="Nombre del nuevo grupo",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "new_group_name",
                "placeholder": "Nombre del grupo",
            }
        ),
    )
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
        groups_qs = Group.objects.order_by(Lower("name"))
        players_qs = (
            player_queryset
            if player_queryset is not None
            else Player.objects.filter(registered_user__isnull=True).select_related("group").order_by(
                Lower("group__name"),
                Lower("name"),
            )
        )
        self.fields["group_id"].queryset = groups_qs
        self.fields["player_id"].queryset = players_qs
        self.fields["player_id"].label_from_instance = (
            lambda player: f"{player.name} — {player.group.name}"
        )
        self.fields["group_choice"].choices = [
            ("", "Crea o Selecciona grupo/club"),
            *[(str(group.pk), group.name) for group in groups_qs],
            (self.GROUP_CHOICE_CREATE, "➕ Crear nuevo grupo/club"),
        ]
        if not self.is_bound and self.initial.get("group_mode") == self.GROUP_MODE_CREATE:
            self.initial["group_choice"] = self.GROUP_CHOICE_CREATE
        self._mark_invalid_fields()

    def _resolved_group(self):
        group_mode = (
            self.cleaned_data.get("group_mode")
            or self.data.get(self.add_prefix("group_mode"))
            or self.GROUP_MODE_JOIN
        )
        if group_mode == self.GROUP_MODE_CREATE:
            return None
        return self.cleaned_data.get("group_id")

    def clean_group_choice(self):
        group_choice = (self.cleaned_data.get("group_choice") or "").strip()
        if not group_choice:
            raise forms.ValidationError("Selecciona un grupo/club o crea uno nuevo.")
        return group_choice

    def _selected_player_for_username_validation(self):
        selected_player = self.cleaned_data.get("player_id")
        if selected_player:
            return selected_player
        if not self.is_bound:
            return None

        raw_player_id = self.data.get(self.add_prefix("player_id"))
        if not raw_player_id:
            return None

        try:
            return self.fields["player_id"].queryset.get(pk=raw_player_id)
        except (Player.DoesNotExist, ValueError, TypeError):
            return None

    def clean_username(self):
        username = (self.cleaned_data.get("username") or "").strip()
        user_exists = User.objects.filter(username__iexact=username).exists()
        selected_player = self._selected_player_for_username_validation()
        player_exists = (
            Player.objects.filter(
                name__iexact=username,
                registered_user__isnull=True,
            )
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

    def clean_email(self):
        email = self.cleaned_data.get("email")
        return validate_unique_email(email)

    def clean(self):
        cleaned_data = super().clean()
        group_choice = cleaned_data.get("group_choice")
        group_mode = self.GROUP_MODE_CREATE if group_choice == self.GROUP_CHOICE_CREATE else self.GROUP_MODE_JOIN
        cleaned_data["group_mode"] = group_mode
        selected_group = None
        if group_mode == self.GROUP_MODE_JOIN and group_choice:
            selected_group = self.fields["group_id"].queryset.filter(pk=group_choice).first()
            cleaned_data["group_id"] = selected_group
        new_group_name = (cleaned_data.get("new_group_name") or "").strip()
        selected_player = cleaned_data.get("player_id")
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if group_mode == self.GROUP_MODE_JOIN:
            if not selected_group:
                self.add_error("group_id", "Selecciona un grupo.")
            if selected_player and selected_group and selected_player.group_id != selected_group.id:
                self.add_error("player_id", "El jugador seleccionado no pertenece a ese grupo.")
        elif group_mode == self.GROUP_MODE_CREATE:
            if not new_group_name:
                self.add_error("new_group_name", "Indica el nombre del nuevo grupo.")
            elif Group.objects.filter(name__iexact=new_group_name).exists():
                self.add_error("new_group_name", "Ya existe un grupo con ese nombre.")
            if selected_player:
                self.add_error("player_id", "No puedes reclamar un jugador existente al crear un grupo nuevo.")

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

        if self.cleaned_data["group_mode"] == self.GROUP_MODE_CREATE:
            group = Group.objects.create(name=self.cleaned_data["new_group_name"].strip())
        else:
            group = self.cleaned_data["group_id"]

        selected_player = self.cleaned_data.get("player_id")
        if selected_player:
            selected_player.registered_user = user
            selected_player.name = user.username
            selected_player.gender = self.cleaned_data["gender"]
            selected_player.group = group
            selected_player.save()
        else:
            Player.objects.create(
                name=user.username,
                registered_user=user,
                gender=self.cleaned_data["gender"],
                group=group,
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

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if normalize_email_for_match(email) == normalize_email_for_match(self.user.email):
            return (email or "").strip()
        return validate_unique_email(email, exclude_user=self.user)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        confirm_email = cleaned_data.get("confirm_email")
        email_errors = self.errors.get("email")

        if normalize_email_for_match(email) != normalize_email_for_match(self.user.email):
            self.show_confirm_email = True
            if email_errors:
                self.add_error(
                    "confirm_email",
                    "Ya existe una cuenta con ese correo electrónico.",
                )
                return cleaned_data
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
