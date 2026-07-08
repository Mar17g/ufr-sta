from flask import Flask, render_template, request, redirect, url_for, session

import mysql.connector

connexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ufr_sta"
)

curseur = connexion.cursor(dictionary=True)

app = Flask(__name__)

app.secret_key = "ufr_stamar"

@app.route('/')
def index():
    curseur = connexion.cursor(dictionary=True)

    curseur.execute("SELECT * FROM UFR_STA WHERE ID_UFR=1")

    ufr = curseur.fetchone()

    curseur.close()

    return render_template("index.html",ufr=ufr)

@app.route('/activites')
def activites():
    return render_template('activites.html')

@app.route('/actualites')
def actualites():
    curseur = connexion.cursor(dictionary=True)
    curseur.execute("SELECT * FROM ACTUALITE ORDER BY DATE_PUBLICATION DESC")
    actualites = curseur.fetchall()
    curseur.close()

    return render_template("actualites.html", actualites=actualites)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/departements')
def departements():
    return render_template('departements.html')

@app.route('/espaceetudiant')
def espaceetudiant():
    return render_template('espaceetudiant.html')

@app.route('/formations')
def formations():
    return render_template('formations.html')

@app.route('/galerie')
def galerie():
    return render_template('galerie.html')

@app.route('/nosenseignants')
def nosenseignants():
    return render_template('nosenseignants.html')

#Le login d'un administrateur
@app.route('/admin/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":

        email = request.form['email']
        motdepasse = request.form['motdepasse']

        curseur = connexion.cursor(dictionary=True)

        sql = "SELECT * FROM UTILISATEUR WHERE EMAIL_USER=%s AND MDP_USER=%s"
        curseur.execute(sql, (email, motdepasse))

        admin = curseur.fetchone()
        curseur.close()

        if admin:
            session["admin"] = admin["ID_USER"]
            return redirect(url_for('dashboard'))

        else:
            return render_template(
                'admin/login.html',
                erreur="Email ou mot de passe incorrect."
            )
    return render_template('admin/login.html')

#Le tablaeu de bord d'un administrateur
@app.route('/admin/dashboard')
def dashboard():

    if "admin" not in session:
        return redirect(url_for('login'))
    return render_template('admin/dashboard.html')

#Gestion des informations de l'ufr
@app.route('/gerer_infoufr', methods=['GET', 'POST'])
def gerer_infoufr():
    if "admin" not in session:
        return redirect(url_for('login'))

    curseur = connexion.cursor(dictionary=True)

    if request.method == "POST":

        nom = request.form['nom']
        sigle = request.form['sigle']
        telephone = request.form['telephone']
        email = request.form['email']
        mot = request.form['mot']
        presentation = request.form['presentation']

        sql = "UPDATE UFR_STA SET NOM_UFR=%s, SIGLE_UFR=%s, TELEPHONE_UFR=%s, EMAIL_UFR=%s, MOT_DU_DIRECTEUR_UFR=%s, PRESENTATION_UFR=%s WHERE ID_UFR=1"

        curseur.execute(sql,(nom,sigle,telephone,email,mot,presentation))

        connexion.commit()

    curseur.execute("SELECT * FROM UFR_STA WHERE ID_UFR=1")

    ufr = curseur.fetchone()

    curseur.close()

    return render_template('admin/gerer_infoufr.html',ufr=ufr)

#Gestion des activités
@app.route('/gerer_act')
def gerer_act():
    return render_template('admin/gerer_act.html')

#Gestion des actualités
@app.route('/admin/gerer_actu', methods=['GET', 'POST'])
def gerer_actu():

    if "admin" not in session:
        return redirect(url_for('login'))

    curseur = connexion.cursor(dictionary=True)

    if request.method == "POST":

        # Supression d'une actualité
        if "supprimer" in request.form:

            id_actu = request.form["id_actu"]

            curseur.execute("DELETE FROM ACTUALITE WHERE ID_ACTU=%s", (id_actu,))
            connexion.commit()

        # Ajout d'une actualité
        else:

            titre = request.form["titre"]
            description = request.form["description"]
            id_photo = request.form["photo"]

            sql = "INSERT INTO ACTUALITE(TITRE_ACTU,DESCRIPTION_ACTU,DATE_PUBLICATION,ID_PHOTO) VALUES(%s,%s,NOW(),%s)"

            curseur.execute(sql,(titre,description,id_photo))
            connexion.commit()

    curseur.execute("SELECT * FROM PHOTO ORDER BY NOM_PHOTO ")
    photos = curseur.fetchall()

    curseur.execute("SELECT * FROM ACTUALITE A INNER JOIN PHOTO P ON A.ID_PHOTO=P.ID_PHOTO ORDER BY DATE_PUBLICATION DESC")

    actualites = curseur.fetchall()
    curseur.close()

    return render_template( "admin/gerer_actu.html", photos=photos, actualites=actualites )

#Gestion des messages reçus
@app.route('/gerer_contact')
def gerer_contact():
    return render_template('admin/gerer_contact.html')

#Gestion des enseignants
@app.route('/gerer_ens')
def gerer_ens():
    return render_template('admin/gerer_ens.html')

#Gestion des formations
@app.route('/gerer_formation')
def gerer_formation():
    return render_template('admin/gerer_formation.html')

#Gestion de la galerie
@app.route('/gerer_galerie')
def gerer_galerie():
    return render_template('admin/gerer_galerie.html')

#La deconexion d'un administrateur
@app.route('/logout')
def logout():

    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)