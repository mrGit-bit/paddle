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
    
    new_players = forms.CharField(
        required=False,
        label="Añade jugadores no registrados (uno por línea)",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Ejemplo1_perez\nEjemplo2_lopez\nEjemplo3_garcia",
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

    def clean(self):
        cleaned = super().clean()
        players = cleaned.get("players")
        num_players = cleaned.get("num_players")
        new_players_raw = cleaned.get("new_players") or ""
        
        # Normalize new player names: one per line, strip, remove empties
        new_names = [line.strip() for line in new_players_raw.splitlines() if line.strip()]
        cleaned["new_player_names"] = new_names  # helper for the view
        
        existing_count = players.count() if players else 0
        total_count = existing_count + len(new_names)
        
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
            
        # Prevent duplicates between selected and new names (case-insensitive)
        if players and new_names:
            existing_names_lower = {p.name.strip().lower() for p in players}
            for name in new_names:
                if name.lower() in existing_names_lower:
                    self.add_error("new_players", f"'{name}' ya existe en la selección.")

        return cleaned
    
    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if len(name) > AMERICANO_NAME_MAX_LEN:
            raise ValidationError(f"El nombre del torneo no puede superar {AMERICANO_NAME_MAX_LEN} caracteres.")
        return name

