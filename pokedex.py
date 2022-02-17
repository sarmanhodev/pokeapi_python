from flask import Flask, render_template, request
import requests
import json
from models.pokeclasse import Pokemon
import random

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/pokemon_search", methods=["GET","POST"])
def buscar_nome():
    pokename = Pokemon("",request.form["nome"].lower(),"","","","","")
    try:
        res = json.loads(requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokename.nome}").text)
        encounter = json.loads(requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokename.nome}/encounters").text) #endpoint que caputra localização
        sprite = res["sprites"]
        sprite = sprite["front_default"]
        pokename.foto = sprite
    
        print("\nnome: "+str(res['name']))

        for i in encounter: #captura localização do pokemon
            pokename.localidade= i['location_area']['name']
        
        if pokename.localidade == "": #verificação caso o pokémon não tenha localização
            pokename.localidade = str("No location")

        print("localização: "+str(pokename.localidade))

        if len(res["types"]) == 2: #captura o tipo do pokemon
            pokename.tipo1 = res["types"][0]['type']['name']
            pokename.tipo2 = " & {}".format(res["types"][1]['type']['name'])
        else:
            pokename.tipo1 = res["types"][0]['type']['name']

        print("type: " + str(pokename.tipo1) +" "+ str(pokename.tipo2))


        poderes = res['moves']
        for i in poderes: #captura os poderes do pokemon de forma aleatória
            power = random.randrange(0,len(poderes))
            pw = poderes[power]
            pokename.moves = pw['move']['name']
        print("move: "+str(pokename.moves) + "\n")

        for i in poderes:
            print(i['move']['name'])
       
    except:
        return render_template("telaerror.html")
    return render_template("template.html", 
    id = res["id"],
    nome = res["name"].upper(),
    localidade = pokename.localidade.upper(),
    tipo1 = pokename.tipo1.upper(),
    tipo2 = pokename.tipo2.upper(),
    moves = pokename.moves.upper(),
    foto = pokename.foto
    )





if __name__=="__main__":
    app.run(debug=True)

