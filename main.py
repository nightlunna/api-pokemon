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
    dicionario_pokemon = request.get_json()

    novo_pokemon = Pokemon(
    nome = dicionario_pokemon ("nome"),
    tipo = dicionario_pokemon ("tipo"),
    nivel = dicionario_pokemon ("nivel"),
    identificador = str(uuid.uuid4())
    )

    pokemons.append(novo_pokemon)
    return jsonify({"msg": "Pokémon criado com sucesso!", "pokemon": novo_pokemon._asdict()})


@app.get("/pokemon/<string:pokemon_id>")
def get_pokemon_by_id(pokemon_id):
    for pokemon in pokemons:
        if pokemon.idenficador == pokemon_id:
            return jsonify(pokemon._asidct())
        
    return jsonify({"erro": "Pokémon não encontrado"}), 404
    