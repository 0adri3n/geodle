from flask import Flask
from flask import render_template, url_for, request, flash, redirect, session

import json

app = Flask(__name__)
app.secret_key = "geodle"

f = open("static/data/data.json", "r", encoding="utf-8")
countries = json.loads(f.read())
names = [i["name"] for i in countries]
f.close()



def getClassicInfo(name):

    country_info = []
    for country in countries:
        if country["name"] == name:
            country_info.append(country["name"])
            country_info.append(country["callingCodes"][0] if country["callingCodes"] else "-")
            country_info.append(country["region"])
            country_info.append(country["population"])
            country_info.append(country["area"] if country["area"] else "-")
            country_info.append(country["timezones"][0] if country["timezones"] else "-")
            break
    return country_info


@app.route('/')
def index(): 
    # f = open("static/data/data.json", "r", encoding="utf-8")
    # pays = json.loads(f.read())
    # f.close()
    # l = 0
    # # Parcourir chaque pays
    # for country in pays:
    #     l+=1
    #     print("Nom du pays :", country["name"])
    #     print("Capitale :", country["capital"])
    #     print("Population :", country["population"])
    #     print("Langues :", ", ".join([lang["name"] for lang in country["languages"]]))
    #     print("Drapeau :", country["flag"])
    #     print("Régions :", country["region"], "-", country["subregion"])
    #     print("-----------------------------------------")
    # print(l)
    session["guesses"] = []
    return render_template('index.html')


@app.route('/classic', methods=["GET", "POST"])
def classic():

    global names

    if request.method == "POST" :

        name = request.form["guess"]
        infos = getClassicInfo(name)
        tries = [t for t in session["guesses"]]

        if infos not in session["guesses"] :
            tries.append(infos)
            session["guesses"] = tries
        else :
            session["guesses"] = tries
        print(session["guesses"])

    headers = ["Name",'Calling code', 'Continent', "Population", "Area", "UTC Time code"]

    return render_template('classic.html', names=names, headers=headers)



if __name__ == '__main__': 

    print("\n---------------------------------------------------------------------\n")
    print("geodle server running\n")
    print("---------------------------------------------------------------------\n")

    app.run(host="127.0.0.1", debug=True)