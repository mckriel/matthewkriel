from django.shortcuts import render
import json

def pokedex_view(request):
    # Load cached Pokémon data
    with open('pokedex/cache/pokemon.json', 'r') as f:
        pokemon_data = json.load(f)
    return render(request, 'pokedex.html', {'pokemon_data': pokemon_data})