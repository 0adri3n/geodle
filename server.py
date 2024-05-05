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
today_flag = daily["flag"]
today_capital = daily["capital"]
today_dns = daily["dns"]



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

def getFlagInfo(name):

    country_info = []
    for country in countries:
        if country["name"] == name:
            country_info.append(country["name"])
            country_info.append(country["region"])
            break
    return country_info


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

@app.route('/flag', methods=["GET", "POST"])
def flag():

    global today_flag
    global names

    if request.method == "POST" :

        name = request.form["guess"]
        infos = getFlagInfo(name)
        tries = [t for t in session["flag_guesses"]]

        if infos not in session["flag_guesses"] :
            tries.append(infos)

        session["flag_guesses"] = tries
        session["flag_cnames"] = [t[0] for t in tries]

        if infos[0] == today_flag[0] :

            session["flag_win"] = True

    headers = ["Name", "Continent"]

    return render_template('flag.html', names=names, headers=headers, today_flag=today_flag)
    
@app.route('/capital', methods=["GET", "POST"])
def capital():

    global today_capital
    global names

    if request.method == "POST" :

        name = request.form["guess"]
        infos = getFlagInfo(name)
        tries = [t for t in session["capital_guesses"]]

        if infos not in session["capital_guesses"] :
            tries.append(infos)

        session["capital_guesses"] = tries
        session["capital_cnames"] = [t[0] for t in tries]

        if infos[0] == today_capital[0] :

            session["capital_win"] = True

    headers = ["Name", "Continent"]

    return render_template('capital.html', names=names, headers=headers, today_capital=today_capital)

@app.route('/dns', methods=["GET", "POST"])
def dns():

    global today_dns
    global names

    if request.method == "POST" :

        name = request.form["guess"]
        infos = getFlagInfo(name)
        tries = [t for t in session["dns_guesses"]]

        if infos not in session["dns_guesses"] :
            tries.append(infos)

        session["dns_guesses"] = tries
        session["dns_cnames"] = [t[0] for t in tries]

        if infos[0] == today_dns[0] :

            session["dns_win"] = True

    headers = ["Name", "Continent"]

    return render_template('dns.html', names=names, headers=headers, today_dns=today_dns)

@app.route('/map', methods=["GET", "POST"])
def map():

    return render_template('map.html')

if __name__ == '__main__': 

    print("\n---------------------------------------------------------------------\n")
    print("geodle server running\n")
    print("---------------------------------------------------------------------\n")

    app.run(host="127.0.0.1", debug=True)