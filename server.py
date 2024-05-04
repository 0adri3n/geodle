from flask import Flask
from flask import render_template, url_for, request, flash, redirect

import json

app = Flask(__name__)
app.secret_key = "geodle"


@app.route('/')
def index(): 
    f = open("static/data/data.json", "r", encoding="utf-8")
    pays = json.loads(f.read())
    f.close()
    l = 0
    # Parcourir chaque pays
    for country in pays:
        l+=1
        print("Nom du pays :", country["name"])
        print("Capitale :", country["capital"])
        print("Population :", country["population"])
        print("Langues :", ", ".join([lang["name"] for lang in country["languages"]]))
        print("Drapeau :", country["flag"])
        print("Régions :", country["region"], "-", country["subregion"])
        print("-----------------------------------------")
    print(l)
    return render_template('index.html')

if __name__ == '__main__': 

    print("\n---------------------------------------------------------------------\n")
    print("geodle server running\n")
    print("---------------------------------------------------------------------\n")

    app.run(host="127.0.0.1", debug=True)