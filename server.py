from flask import Flask, render_template, request, url_for, session
import json
from os.path import join, dirname, realpath

app = Flask(__name__)
app.config['DATA_DIR'] = join(dirname(realpath(__file__)),'static')
app.secret_key = b'99b45274a4b2da7440ab249f17e718688b53b646f3dd57f23a9b29839161749f'

@app.route("/")
def index(): 
    session["erreur"] = False
    return render_template('bienvenue.html')

@app.route("/inscription")
def demande(): 
    return render_template('inscription.html')

@app.route("/connection")
def demande2(): 
    return render_template('connection.html')

@app.route("/accueil_inscri", methods=['POST'])
def accueil_inscri():
    session["mdp"]=request.form['mdp']
    session["username"]=request.form['nom']
    email=request.form['email']
    with open(join(app.config['DATA_DIR'],'user.json'), 'r') as f:
        auth = json.load(f)
        for m in auth :
            if session["username"] == m["Nom"]:
                session["erreur"] = True
                return render_template("inscription.html", erreur = session["erreur"])
        auth.append(
            {"Nom":session["username"], 
             "Mdp":session["mdp"], 
             "Email": email, 
             "Coins": 100, 
             "demandes": []}
        )
    with open(join(app.config['DATA_DIR'],'user.json'), 'w') as f:
        json.dump(auth, f, ensure_ascii=True)
    with open(join(app.config['DATA_DIR'],'data.json'), 'r') as f:
        don = json.load(f)
    return render_template("accueil.html", name = session["username"], dem = don)

@app.route("/accueil_connec", methods=["POST"])
def accueil_connec(): 
    session["username"]=request.form["nom"]
    session["mdp"]=request.form["mdp"]
    with open(join(app.config['DATA_DIR'],'user.json'), 'r') as f:
        auth = json.load(f)
        for i in auth:
            if i["Nom"] == session["username"] and i["Mdp"] == session["mdp"]:
                with open(join(app.config['DATA_DIR'],'data.json'), 'r') as f:
                    dem = json.load(f)
                return render_template('accueil.html', name = session["username"], dem = dem)
    session["erreur"] = True
    return render_template('connection.html', erreur = session["erreur"])    

@app.route("/accueil", methods=["GET","POST"])
def acceuil(): 
    with open(join(app.config['DATA_DIR'],'data.json'), 'r') as f:
        dem = json.load(f)
    return render_template('accueil.html', dem = dem, name = session["username"])

@app.route("/show", methods=["POST"])
def show(): 
    filtre_pseudo = request.form['choix_pseudo']
    filtre_matiere = request.form['choix_matiere']
    with open(join(app.config['DATA_DIR'],'data.json'), 'r') as f:
        dem = json.load(f)
    if filtre_matiere != "" and filtre_pseudo != "":
        return render_template('filtre_2.html', dem = dem, filtre_pseudo=filtre_pseudo, filtre_matiere=filtre_matiere)
    if filtre_matiere == "" and filtre_pseudo != "":
         return render_template('filtre_pseu.html', dem = dem, filtre_pseudo=filtre_pseudo, filtre_matiere=filtre_matiere)
    if filtre_matiere != "" and filtre_pseudo == "":
        return render_template('filtre_mat.html', dem = dem, filtre_pseudo=filtre_pseudo, filtre_matiere=filtre_matiere)

@app.route("/creation",  methods=["POST"])
def creation(): 
    matiere = request.form["matiere"]
    com = request.form["com"]
    prix = int(request.form["prix"])
    with open(join(app.config['DATA_DIR'],'data.json'), 'r') as f:
        dem = json.load(f)
        dem.append(
            {
            "pseudo": session["username"],
            "matiere": matiere,
            "commentaire": com,
            "prix": prix
            }
        )
    with open(join(app.config['DATA_DIR'],'data.json'), 'w') as f:
        json.dump(dem, f)
    with open(join(app.config['DATA_DIR'],'user.json'), 'r') as q:
        crea = json.load(q)
        for u in crea :
            if u["Nom"] == session["username"]:
                u["demandes"].append(
                    {"matiere": matiere,
                     "commentaire": com,
                     "prix": prix}
                )
    with open(join(app.config['DATA_DIR'],'user.json'), 'w') as q:
        json.dump(crea, q)
    return render_template('accueil.html', dem = dem, name = session["username"])
    
@app.route("/profil", methods=["GET", "POST"])
def profil(): 
    with open(join(app.config['DATA_DIR'],'data.json'), 'r') as q:
        dem = json.load(q)
    return render_template('profil.html', dem= dem, name = session["username"], mdp = session["mdp"])

@app.route("/chat", methods=["GET", "POST"])
def chat(): 
    client = request.form[client]
    return render_template('chat.html')

app.run(host = '127.0.0.1', port='5000', debug=True)