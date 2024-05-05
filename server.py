from flask import Flask
from flask import render_template, url_for, request, flash, redirect, session

import json
import yaml

app = Flask(__name__)
app.secret_key = "geodle"

f = open("static/data/data.json", "r", encoding="utf-8")
countries = json.loads(f.read())
names = [i["name"] for i in countries]
f.close()

daily_f = open("static/config/daily.yaml", "r", encoding="utf-8")
daily = yaml.safe_load(daily_f)
daily_f.close()
classic_country = daily["classic"]



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

    # Initialisation des cookies

    session["guesses"] = []
    session["win"] = False
    session["classic_tcount"] = []

    return render_template('index.html')


@app.route('/classic', methods=["GET", "POST"])
def classic():

    global names
    global classic_country

    

    if request.method == "POST" :

        name = request.form["guess"]
        infos = getClassicInfo(name)
        tries = [t for t in session["guesses"]]

        if infos not in session["guesses"] :
            tries.append(infos)

        session["guesses"] = tries
        session["classic_tcount"] = [t[0] for t in tries]

        if infos == classic_country :

            session["win"] = True

    headers = ["Name",'Calling code', 'Continent', "Population", "Area", "UTC Time code"]
    return render_template('classic.html', names=names, headers=headers, classic_country=classic_country)



if __name__ == '__main__': 

    print("\n---------------------------------------------------------------------\n")
    print("geodle server running\n")
    print("---------------------------------------------------------------------\n")

    app.run(host="127.0.0.1", debug=True)