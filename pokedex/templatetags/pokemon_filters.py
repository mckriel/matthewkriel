from django import template

register = template.Library()

TYPE_COLORS = {
    "fire": "255, 180, 142",      # Brighter Light Salmon (Fire)
    "water": "155, 226, 255",     # Brighter Sky Blue (Water)
    "grass": "172, 271, 172",     # Brighter Pale Green (Grass)
    "electric": "255, 255, 50",   # Brighter Yellow (Electric)
    "psychic": "255, 125, 200",   # Brighter Pink (Psychic)
    "ice": "193, 236, 250",       # Brighter Light Blue (Ice)
    "dragon": "158, 63, 246",     # Brighter Blue Violet (Dragon)
    "dark": "132, 148, 164",      # Brighter Slate Gray (Dark)
    "fairy": "255, 202, 213",     # Brighter Light Pink (Fairy)
    "normal": "231, 231, 231",    # Brighter Light Gray (Normal)
    "fighting": "225, 112, 112",  # Brighter Indian Red (Fighting)
    "flying": "155, 226, 270",    # Brighter Light Sky Blue (Flying)
    "poison": "167, 132, 239",    # Brighter Medium Purple (Poison)
    "ground": "230, 200, 160",    # Brighter Tan (Ground)
    "rock": "204, 154, 31",       # Brighter Dark Goldenrod (Rock)
    "bug": "174, 225, 70",        # Brighter Yellow Green (Bug)
    "ghost": "95, 20, 150",       # Brighter Indigo (Ghost)
    "steel": "212, 212, 212",     # Brighter Silver (Steel)
}

@register.filter
def color_tint(type_name):
    return TYPE_COLORS.get(type_name, "255, 255, 255")  # Default to white