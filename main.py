from flask import Flask, request, jsonify
from typing import NamedTuple
import uuid

app = Flask(__name__)

class Pokemon(NamedTuple):
    nome: str
    tipo: str
    nivel: int
    identificador: str

pokemons: list[Pokemon] = []

@app.post("/pokemon")
def criar_pokemon():
    dicionario_pokemon = request.get_json()

    novo_pokemon = Pokemon(
    nome = dicionario_pokemon.get ("nome"),
    tipo = dicionario_pokemon.get ("tipo"),
    nivel = dicionario_pokemon.get ("nivel"),
    identificador = str(uuid.uuid4())
    )

    pokemons.append(novo_pokemon)
    return jsonify({"msg": "Pokémon criado com sucesso!", "pokemon": novo_pokemon._asdict()}), 200


@app.get("/pokemon/<string:pokemon_id>")
def get_pokemon_by_id(pokemon_id):
    for pokemon in pokemons:
        if pokemon.identificador == pokemon_id:
            return jsonify(pokemon._asdict())
        
    return jsonify({"erro": "Pokémon não encontrado"}), 404

@app.get("/pokemon")
def listar_pokemon():
    pokemons_dicionario = [pokemon._asdict() for pokemon in pokemons]
    
    return jsonify(pokemons_dicionario), 200


@app.put("/pokemon/<string:pokemon_id>")
def atualizar_pokemon(pokemon_id):
    atualizar = request.get_json()

    for indice, pokemon in enumerate(pokemons):
        if pokemon.identificador == pokemon_id:
            pokemon_atualizado = Pokemon(
                nome = atualizar.get("nome", pokemon.nome),
                tipo = atualizar.get("tipo", pokemon.tipo),
                nivel = atualizar.get("nivel", pokemon.nivel),
                identificador = pokemon.identificador 
            )

            pokemons[indice] = pokemon_atualizado

            return jsonify ({"msg": "Pokémon atualizado!", "pokemon": pokemon_atualizado._asdict()}), 200
        

@app.delete("/pokemon/<string:pokemon_id>")
def excluir_pokemon(pokemon_id):
    for pokemon in pokemons:
        if pokemon.identificador == pokemon_id:
            pokemons.remove(pokemon)
            return jsonify({"msg": "Pokémon excluído com sucesso!"}), 200
        
    return jsonify ({"error": "Pokémon não encontrado"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

    