import json
from django.core.management.base import BaseCommand
import requests

def fetch_pokemon_data():
    pokemon_list = []
    for id in range(1, 152):
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
        data = response.json()
        pokemon_list.append({
            "id": data["id"],
            "name": data["name"],
            "types": [t["type"]["name"] for t in data["types"]],
            "image_url": data["sprites"]["other"]["official-artwork"]["front_default"]
        })
        print(f"Fetched data for Pokemon: {id}")
    return pokemon_list

class Command(BaseCommand):
    help = "Fetches Pokémon data from PokeAPI and saves it to a JSON file"

    def handle(self, *args, **kwargs):
        data = fetch_pokemon_data()
        with open('pokedex/cache/pokemon.json', 'w') as f:
            json.dump(data, f)
        self.stdout.write("Successfully cached Pokémon data!")