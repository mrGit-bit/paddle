"""Central medal metadata for the public Medallero page."""

MEDAL_DEFINITIONS = [
    {
        "key": "first_place",
        "name": "Primer puesto",
        "icon": "🥇",
        "description": "Ocupa la primera posición de su ranking.",
        "category": "position",
        "scopes": ["all", "male", "female", "mixed"],
        "order": 1,
    },
    {
        "key": "second_place",
        "name": "Segundo puesto",
        "icon": "🥈",
        "description": "Ocupa la segunda posición de su ranking.",
        "category": "position",
        "scopes": ["all", "male", "female", "mixed"],
        "order": 2,
    },
    {
        "key": "third_place",
        "name": "Tercer puesto",
        "icon": "🥉",
        "description": "Ocupa la tercera posición de su ranking.",
        "category": "position",
        "scopes": ["all", "male", "female", "mixed"],
        "order": 3,
    },
    {
        "key": "top3_efficiency",
        "name": "Top 3 eficacia",
        "icon": "🎯",
        "description": "Está entre los tres jugadores con mejor eficacia dentro de la primera página.",
        "category": "performance",
        "scopes": ["all", "male", "female", "mixed"],
        "order": 4,
    },
    {
        "key": "top3_matches",
        "name": "Top 3 partidos",
        "icon": "🏓",
        "description": "Está entre los tres jugadores con más partidos disputados dentro de la primera página.",
        "category": "performance",
        "scopes": ["all", "male", "female", "mixed"],
        "order": 5,
    },
    {
        "key": "cuadro_honor",
        "name": "Cuadro de honor",
        "icon": "🏆",
        "description": "Forma parte de la primera página del ranking.",
        "category": "participation",
        "scopes": ["all", "male", "female", "mixed"],
        "order": 6,
    },
]

SCOPE_CONFIG = {
    "all": {
        "label": "Todos",
        "css_class": "medal-scope-all",
        "progress_color_class": "circular-progress-primary",
    },
    "male": {
        "label": "Masculino",
        "css_class": "medal-scope-male",
        "progress_color_class": "circular-progress-success",
    },
    "female": {
        "label": "Femenino",
        "css_class": "medal-scope-female",
        "progress_color_class": "circular-progress-success",
    },
    "mixed": {
        "label": "Mixtos",
        "css_class": "medal-scope-mixed",
        "progress_color_class": "circular-progress-warning",
    },
}
