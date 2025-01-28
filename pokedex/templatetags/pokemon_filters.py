from django import template

register = template.Library()

TYPE_COLORS = {
    "normal": "168, 168, 120",  # Keep subtle for balance
"fire": "255, 107, 107",    # Bright red
"water": "78, 205, 196",   # Turquoise
"electric": "255, 217, 61",# Neon yellow
"grass": "108, 190, 71",   # Lime green
"ice": "126, 232, 250",     # Bright cyan
"fighting": "255, 94, 94",# Intense red
"poison": "200, 107, 250",  # Electric purple
"ground": "230, 177, 67",  # Golden yellow
"flying": "137, 196, 244",  # Sky blue
"psychic": "255, 119, 168", # Hot pink
"bug": "163, 198, 57",     # Acid green
"rock": "197, 168, 128",    # Warm sand
"ghost": "155, 89, 182",   # Vivid purple
"dragon": "108, 92, 231",  # Royal blue
"dark": "90, 90, 90",    # Dark gray (kept subtle)
"steel": "180, 180, 180",   # Silver
"fairy": "255, 181, 232",   # Bright pink
}

@register.filter
def color_tint(type_name):
    return TYPE_COLORS.get(type_name, "255, 255, 255")  # Default to white