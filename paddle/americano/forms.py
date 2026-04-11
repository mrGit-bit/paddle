# americano/forms.py
from django import forms
from django.db.models.functions import Lower
from django.utils import timezone
from django.core.exceptions import ValidationError

from games.models import Player
from .models import AmericanoTournament

AMERICANO_NAME_MAX_LEN = 26  # len("with existing players only")

class AmericanoTournamentForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all().order_by(Lower("name")),
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 8}),
        required=True,
        label="Escoge jugadores registrados*",
    )
    
    new_players_male = forms.CharField(
        required=False,
        label="Añade jugadores no registrados (uno por línea) - Masculino",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Jugador1\nJugador2",
            }
        ),
    )
    new_players_female = forms.CharField(
        required=False,
        label="Añade jugadoras no registradas (una por línea) - Femenino",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Jugadora1\nJugadora2",
            }
        ),
    )

    class Meta:
        model = AmericanoTournament
        fields = ["name", "play_date", "num_players", "players"]        
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control", 
                "required": True, 
                "maxlength": AMERICANO_NAME_MAX_LEN
            }),
            "play_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
                "required": True,
            }),
            "num_players": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 4,
                "required": True,
            }),            
        }

        labels = {
            "name": "Nombre del torneo*",
            "play_date": "Fecha torneo*",
            "num_players": "Nº jugadores*",            
        }

    def __init__(self, *args, group=None, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = Player.objects.all().select_related("group").order_by(Lower("name"))
        if group is not None:
            queryset = queryset.filter(group=group)
        self.fields["players"].queryset = queryset
        self.group = group

    def clean(self):
        cleaned = super().clean()
        players = cleaned.get("players")
        num_players = cleaned.get("num_players")
        new_male_raw = cleaned.get("new_players_male") or ""
        new_female_raw = cleaned.get("new_players_female") or ""

        new_male_names = [line.strip() for line in new_male_raw.splitlines() if line.strip()]
        new_female_names = [line.strip() for line in new_female_raw.splitlines() if line.strip()]
        new_entries = (
            [(name, Player.GENDER_MALE) for name in new_male_names]
            + [(name, Player.GENDER_FEMALE) for name in new_female_names]
        )
        cleaned["new_player_entries"] = new_entries  # helper for the view

        existing_count = players.count() if players else 0
        total_count = existing_count + len(new_entries)

        play_date = cleaned.get("play_date")
        today = timezone.localdate()

        if play_date and play_date < today:
            self.add_error(
                "play_date",
                "La fecha de juego no puede ser anterior a la fecha de creación.",
            )               

        if num_players and total_count != num_players:
            self.add_error(
                None,
                "El número de jugadores añadidos al torneo debe coincidir con el número de jugadores.",
            )

        if num_players and num_players % 4 != 0:
            self.add_error(
                "num_players",
                "El número de jugadores debe ser múltiplo de 4.",
            )

        selected_names_lower = {p.name.strip().lower() for p in players} if players else set()
        typed_by_name: dict[str, str] = {}

        for name, gender in new_entries:
            name_l = name.lower()
            if name_l in selected_names_lower:
                self.add_error(
                    None,
                    f"'{name}' ya existe en la selección de jugadores registrados.",
                )

            prev_gender = typed_by_name.get(name_l)
            if prev_gender and prev_gender != gender:
                self.add_error(None, f"'{name}' está repetido con distinto género.")
            typed_by_name[name_l] = gender

            existing = Player.objects.filter(name__iexact=name, group=self.group).first() if self.group else Player.objects.filter(name__iexact=name).first()
            if existing and existing.gender and existing.gender != gender:
                self.add_error(
                    None,
                    f"'{name}' ya existe con género distinto en la base de datos.",
                )

        return cleaned
    
    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if len(name) > AMERICANO_NAME_MAX_LEN:
            raise ValidationError(f"El nombre del torneo no puede superar {AMERICANO_NAME_MAX_LEN} caracteres.")
        return name
