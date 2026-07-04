from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/activites')
def activites():
    return render_template('activites.html')

@app.route('/actualites')
def actualites():
    return render_template('actualites.html')

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




if __name__ == '__main__':
    app.run(debug=True)