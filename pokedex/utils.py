import requests

def fetch_pokemon_data():
    pokemon_list = []
    for id in range(1, 152):  # 151 Pokémon
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
        data = response.json()
        pokemon_list.append({
            "id": data["id"],
            "name": data["name"],
            "types": [t["type"]["name"] for t in data["types"]],
            "image_url": data["sprites"]["other"]["official-artwork"]["front_default"]
        })
    return pokemon_list