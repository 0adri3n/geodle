from flask import Flask
from flask import render_template, url_for, request, flash, redirect, session

import json
import yaml

import folium

from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = "geodle"



def insert_spaces(number):
    number_str = str(number)
    if len(number_str) <= 3:
        return number_str
    else:
        parts = []
        while len(number_str) > 3:
            parts.append(number_str[-3:])
            number_str = number_str[:-3]
        parts.append(number_str)
        return " ".join(reversed(parts))

def getClassicInfo(name):

    country_info = []
    for country in countries:
        if country["name"] == name:
            country_info.append(country["name"])
            country_info.append(country["callingCodes"][0] if country["callingCodes"] else "-")
            country_info.append(country["region"])
            country_info.append(insert_spaces(country["population"]))
            country_info.append(insert_spaces(country["area"] if country["area"] else "-"))
            country_info.append(country["timezones"][0] if country["timezones"] else "-")
            break
    return country_info

def getFlagInfo(name):

    country_info = []
    for country in countries:
        if country["name"] == name:
            country_info.append(country["name"])
            country_info.append(country["region"])
            break
    return country_info

f = open("static/data/data.json", "r", encoding="utf-8")
countries = json.loads(f.read())
names = [i["name"] for i in countries]
f.close()

daily_f = open("static/config/daily.yaml", "r", encoding="utf-8")
daily = yaml.safe_load(daily_f)
daily_f.close()
classic_country = getClassicInfo(daily["classic"][0])
print(classic_country)
print(daily["classic"])
today_flag = daily["flag"]
today_capital = daily["capital"]
today_dns = daily["dns"]
today_marker = daily["map"]

@app.route('/')
def index():

    # Initialisation des cookies
    # Classic mode
    session["guesses"] = []
    session["win"] = False
    session["classic_tcount"] = []
    
    # Flag mode
    session["flag_win"] = False
    session["flag_guesses"] = []
    session["flag_cnames"] = []

    # Capital mode
    session["capital_win"] = False
    session["capital_guesses"] = []
    session["capital_cnames"] = []

    # DNS mode
    session["dns_win"] = False
    session["dns_guesses"] = []
    session["dns_cnames"] = []

    # Map mode
    session["map_win"] = False
    session["map_guesses"] = []
    session["map_cnames"] = []

    checkTimes()

    return render_template('index.html')


@app.route('/classic', methods=["GET", "POST"])
def classic():

    global names
    global classic_country

    if request.method == "POST" :
        name = request.form["guess"]
        if name in names :
            infos = getClassicInfo(name)
            tries = [t for t in session["guesses"]]
            
            if infos not in session["guesses"] :
                tries.insert(0, infos)

            session["guesses"] = tries
            session["classic_tcount"] = [t[0] for t in tries]
            print(infos)
            print(classic_country)
            print(session["guesses"])
            if infos == classic_country :
                session["win"] = True
        else:
            flash("Please enter a correct country.")

    headers = ["Name",'Calling code', 'Continent', "Population", "Area", "UTC Time code"]
    return render_template('classic.html', names=names, headers=headers, classic_country=classic_country)

@app.route('/flag', methods=["GET", "POST"])
def flag():

    global today_flag
    global names

    if request.method == "POST" :

        name = request.form["guess"]
        if name in names :
            infos = getFlagInfo(name)
            tries = [t for t in session["flag_guesses"]]

            if infos not in session["flag_guesses"] :
                tries.insert(0, infos)

            session["flag_guesses"] = tries
            session["flag_cnames"] = [t[0] for t in tries]

            if infos[0] == today_flag[0] :

                session["flag_win"] = True
        else:
            flash("Please enter a correct country.")

    headers = ["Name", "Continent"]

    return render_template('flag.html', names=names, headers=headers, today_flag=today_flag)
    
@app.route('/capital', methods=["GET", "POST"])
def capital():

    global today_capital
    global names

    if request.method == "POST" :

        name = request.form["guess"]
        if name in names :
            infos = getFlagInfo(name)
            tries = [t for t in session["capital_guesses"]]

            if infos not in session["capital_guesses"] :
                tries.insert(0, infos)

            session["capital_guesses"] = tries
            session["capital_cnames"] = [t[0] for t in tries]

            if infos[0] == today_capital[0] :

                session["capital_win"] = True
        else:
            flash("Please enter a correct country.")


    headers = ["Name", "Continent"]

    return render_template('capital.html', names=names, headers=headers, today_capital=today_capital)

@app.route('/dns', methods=["GET", "POST"])
def dns():

    global today_dns
    global names

    if request.method == "POST" :

        name = request.form["guess"]
        if name in names :
            infos = getFlagInfo(name)
            tries = [t for t in session["dns_guesses"]]
            if infos not in session["dns_guesses"] :
                tries.insert(0, infos)

            session["dns_guesses"] = tries
            session["dns_cnames"] = [t[0] for t in tries]

            if infos[0] == today_dns[0] :

                session["dns_win"] = True

        else:
            flash("Please enter a correct country.")

    headers = ["Name", "Continent"]

    return render_template('dns.html', names=names, headers=headers, today_dns=today_dns)

@app.route('/map', methods=["GET", "POST"])
def map():

    global today_marker
    global names

    lat, long = today_marker[1], today_marker[2]
    
    if not session["map_win"] :

        m = folium.Map(location=[20, 20], zoom_start=2, maxZoom=20)
        folium.TileLayer('cartodbpositronnolabels').add_to(m)

        fg = folium.FeatureGroup(name="", control=False).add_to(m)
        folium.Marker(location=(lat, long)).add_to(fg)

        # set the iframe width and height
        m.get_root().width = "600px"
        m.get_root().height = "400px"
        iframe = m.get_root()._repr_html_()

    if request.method == "POST" :

        name = request.form["guess"]
        if name in names :
            infos = getFlagInfo(name)
            tries = [t for t in session["map_guesses"]]

            if infos not in session["map_guesses"] :
                tries.insert(0, infos)

            session["map_guesses"] = tries
            session["map_cnames"] = [t[0] for t in tries]

            if infos[0] == today_marker[0] :

                
                session["map_win"] = True
                m = folium.Map(location=[lat, long], zoom_start=7)
                folium.TileLayer('cartodbpositronnolabels').add_to(m)

                fg = folium.FeatureGroup(name=infos[0], control=False).add_to(m)
                icon = folium.Icon(color="green", icon="ok-sign")
                folium.Marker(location=(lat, long), popup=infos[0], icon=icon).add_to(fg)                

                # set the iframe width and height
                m.get_root().width = "600px"
                m.get_root().height = "400px"
                iframe = m.get_root()._repr_html_()

        else:
            flash("Please enter a correct country.")

    headers = ["Name", "Continent"]

    return render_template('map.html', names=names, headers=headers, today_marker=today_marker, iframe=iframe)

def checkTimes():

    global daily
    global classic_country
    global today_flag
    global today_capital
    global today_dns
    global today_marker

    # Récupérer l'heure actuelle
    current_time = datetime.now().time()

    # Extraire l'heure de l'objet time
    current_hour = current_time.hour

    # Vérifier si l'heure actuelle est le matin (minuit à midi)
    if 0 <= current_hour < 12:
        if not daily["morning_edit"]:
            with open("static/config/daily.yaml", "r", encoding="utf-8") as yaml_file:
                data = yaml.safe_load(yaml_file)

            # Modifier la valeur
            data["morning_edit"] = True
            data["afternoon_edit"] = False

            # Sauvegarder les modifications dans le fichier YAML
            with open("static/config/daily.yaml", "w", encoding="utf-8") as yaml_file:
                yaml.dump(data, yaml_file)

            daily_f = open("static/config/daily.yaml", "r", encoding="utf-8")
            daily = yaml.safe_load(daily_f)
            daily_f.close()
            classic_country = daily["classic"]
            today_flag = daily["flag"]
            today_capital = daily["capital"]
            today_dns = daily["dns"]
            today_marker = daily["map"]

            changeGuesses()

    # Vérifier si l'heure actuelle est l'après-midi (midi à 23h59)
    elif 12 <= current_hour <= 23:
        if not daily["afternoon_edit"]:
            with open("static/config/daily.yaml", "r", encoding="utf-8") as yaml_file:
                data = yaml.safe_load(yaml_file)

            # Modifier la valeur
            data["morning_edit"] = False
            data["afternoon_edit"] = True

            # Sauvegarder les modifications dans le fichier YAML
            with open("static/config/daily.yaml", "w", encoding="utf-8") as yaml_file:
                yaml.dump(data, yaml_file)

            daily_f = open("static/config/daily.yaml", "r", encoding="utf-8")
            daily = yaml.safe_load(daily_f)
            daily_f.close()
            classic_country = daily["classic"]
            today_flag = daily["flag"]
            today_capital = daily["capital"]
            today_dns = daily["dns"]
            today_marker = daily["map"]
    
            changeGuesses()


def changeGuesses():

    print("Guesses changed | " + str(datetime.now().time()))

    global daily
    global classic_country
    global today_flag
    global today_capital
    global today_dns
    global today_marker

    # Charger le fichier JSON
    with open("static/data/data.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    random_indexes = [random.randint(0, 249) for i in range(5)]

    new_classic = data[random_indexes[0]]
    new_classic = [new_classic["name"], new_classic["callingCodes"][0], new_classic["region"], new_classic["population"], new_classic["area"], new_classic["timezones"][0]]
    new_capital = data[random_indexes[1]]
    new_capital = [new_capital["name"], new_capital["region"], new_capital["capital"]]
    new_dns = data[random_indexes[2]]
    new_dns = [new_dns["name"], new_dns["region"], new_dns["topLevelDomain"][0]]
    new_flag = data[random_indexes[3]]
    new_flag = [new_flag["name"], new_flag["region"], new_flag["alpha2Code"]]
    new_map = data[random_indexes[4]]
    new_map = [new_map["name"], new_map["latlng"][0], new_map["latlng"][1], new_map["region"]]

    with open("static/config/daily.yaml", "r", encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)

    # Modifier la valeur
    data["capital"] = new_capital
    data["classic"] = new_classic
    data["dns"] = new_dns
    data["flag"] = new_flag
    data["map"] = new_map

    # Sauvegarder les modifications dans le fichier YAML
    with open("static/config/daily.yaml", "w", encoding="utf-8") as yaml_file:
        yaml.dump(data, yaml_file)

    daily_f = open("static/config/daily.yaml", "r", encoding="utf-8")
    daily = yaml.safe_load(daily_f)
    daily_f.close()
    classic_country = daily["classic"]
    today_flag = daily["flag"]
    today_capital = daily["capital"]
    today_dns = daily["dns"]
    today_marker = daily["map"]


if __name__ == '__main__': 

    print("\n---------------------------------------------------------------------\n")
    print("geodle server running\n")
    print("---------------------------------------------------------------------\n")

    app.run(host="127.0.0.1", debug=True)
