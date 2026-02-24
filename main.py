from flask import Flask, request, jsonify
from typing import NamedTuple
import uuid

app = Flask(__name__)

class Pokemon(NamedTuple):
    nome: str
    tipo: str
    nivel: int
    idenficador: str

pokemons: list[Pokemon] = []

@app.post("/pokemon")
def criar_pokemon():
    dicionario_python = request.get_json()

    novo_pokemon = Pokemon(
    nome = dicionario_python ("nome"),
    tipo = dicionario_python ("tipo"),
    nivel = dicionario_python ("nivel"),
    identificador = str(uuid.uuid4())
    )

    pokemons.append(novo_pokemon)
    return jsonify({"msg": "Pokémon criado com sucesso!", "pokemon": novo_pokemon._asdict()})


@app.get("/pokemon/<string:pokemon_id>")
def get_pokemon_by_id(pokemon_id):
    for pokemon in pokemons:
        if pokemon.idenficador == pokemon_id:
            return jsonify(pokemon._asidct())
        
    return jsonify({"error": "Pokémon não encontrado"}), 404
    