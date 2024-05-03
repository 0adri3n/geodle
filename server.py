from flask import Flask
from flask import render_template, url_for, request, flash, redirect

app = Flask(__name__)
app.secret_key = "geodle"


@app.route('/')
def index(): 

    return render_template('index.html')

if __name__ == '__main__': 

    print("\n---------------------------------------------------------------------\n")
    print("geodle server running\n")
    print("---------------------------------------------------------------------\n")

    app.run(host="127.0.0.1", debug=True)