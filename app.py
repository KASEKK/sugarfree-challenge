from flask import Flask, render_template, request, redirect
from plyer import notification
import json
from datetime import datetime

app = Flask(__name__)

# Variables globales
motivation = ""
compteur_jours = 0

# Fonction pour envoyer des notifications
def send_notification():
    notification.notify(
        title="Sevrage Sucre",
        message="Continuez, vous êtes sur la bonne voie !",
        timeout=10
    )

# Fonction pour calculer les jours sans sucre
def calculate_days(start_date):
    today = datetime.today()
    delta = today - start_date
    return delta.days

@app.route('/', methods=['GET', 'POST'])
def index():
    global motivation, compteur_jours
    if request.method == 'POST':
        # Si l'utilisateur entre ses motivations
        motivation = request.form.get('motivation')
        start_date = datetime.today()
        compteur_jours = calculate_days(start_date)
        # Sauvegarder les données
        with open('data/motivations.json', 'w') as f:
            json.dump({'motivation': motivation, 'start_date': start_date.strftime("%Y-%m-%d")}, f)

    return render_template('index.html', motivation=motivation, compteur_jours=compteur_jours)

@app.route('/reset', methods=['POST'])
def reset():
    global compteur_jours
    compteur_jours = 0
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
