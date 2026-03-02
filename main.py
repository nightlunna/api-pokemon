import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import NamedTuple
import uuid

app = Flask(__name__)
CORS(app)

def conectar_bancodedados():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "pokedex"
    )

class Pokemon(NamedTuple):
    nome: str
    tipo: str
    nivel: int
    hp: int
    ataque: int
    defesa: int
    ataque_especial: int
    defesa_especial: int
    velocidade: int
    identificador: str
    imagem: str
        
pokemons: list[Pokemon] = []

@app.post("/pokemon")
def criar_pokemon():
    dicionario_pokemon = request.get_json()
    gerado_id = str(uuid.uuid4())

    try:
        conn = conectar_bancodedados()
        cursor = conn.cursor()

        sql = """insert into pokemons
        ( identificador, nome, tipo, nivel, hp, ataque, defesa, ataque_especial, defesa_especial, velocidade, imagem )
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """""

        valores = (
            gerado_id,
            dicionario_pokemon.get ("nome"),
            dicionario_pokemon.get ("tipo"),
            dicionario_pokemon.get ("nivel", 0),
            dicionario_pokemon.get ("hp", 0),
            dicionario_pokemon.get ("ataque", 0),
            dicionario_pokemon.get ("defesa", 0),
            dicionario_pokemon.get ("ataque_especial", 0),
            dicionario_pokemon.get ("defesa_especial", 0),
            dicionario_pokemon.get("velocidade", 0),
            dicionario_pokemon.get("imagem","" )
        )
  
        cursor.execute(sql, valores)
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"msg": "Pokémon gravado no banco de dados", "id": gerado_id}), 201

    except Exception as e:
        return jsonify({"erro": f"Falha no banco: {str(e)}"}, 500)


@app.get("/pokemon/<string:pokemon_id>")
def get_pokemon_by_id(pokemon_id):
    for pokemon in pokemons:
        if pokemon.identificador == pokemon_id:
            return jsonify(pokemon._asdict())
        
    return jsonify({"erro": "Pokémon não encontrado"}), 404

@app.get("/pokemon")
def listar_pokemon():
    try:
        conn= conectar_bancodedados()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pokemons")

        pokemons_dicionario = cursor.fetchall()
        cursor.close()
        conn.close()
    
        return jsonify(pokemons_dicionario), 200
    
    except Exception as e: 
        return jsonify({"erro": f"Pokemon não encontrado: {str(e)}"}), 500


@app.put("/pokemon/<string:pokemon_id>")
def atualizar_pokemon(pokemon_id):
    atualizar = request.get_json()

    for indice, pokemon in enumerate(pokemons):
        if pokemon.identificador == pokemon_id:
            pokemon_atualizado = Pokemon(
                nome = atualizar.get("nome", pokemon.nome),
                tipo = atualizar.get("tipo", pokemon.tipo),
                nivel = atualizar.get("nivel", pokemon.nivel),
                hp = atualizar.get("hp", pokemon.hp),
                ataque = atualizar.get("ataque", pokemon.ataque),
                defesa = atualizar.get("defesa", pokemon.defesa),
                ataque_especial = atualizar.get("ataque_especial", pokemon.ataque_especial),
                defesa_especial = atualizar.get("defesa_especial", pokemon.defesa_especial),
                velocidade = atualizar.get("velocidade", pokemon.velocidade),
                identificador = pokemon.identificador,
                imagem = atualizar.get ("imagem", pokemon.imagem)
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

    