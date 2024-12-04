from flask import Flask, render_template_string, request, redirect, url_for
import json, os, threading, random, requests

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

# HTML pour la page
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Vocal Channel Manager</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1e1e2f;
            color: #fff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #2b2b3c;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
            width: 400px;
            text-align: center;
        }
        h1 {
            margin-bottom: 20px;
            font-size: 24px;
        }
        label {
            display: block;
            margin-bottom: 10px;
            text-align: left;
        }
        input[type="text"], input[type="number"], select {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #555;
            border-radius: 4px;
            background-color: #333;
            color: #fff;
        }
        input[type="submit"] {
            background-color: #007bff;
            color: #fff;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Vocal Channel Manager</h1>
        <form method="post" action="/">
            <h2>Ajouter un utilisateur</h2>
            <input type="hidden" name="action" value="add_user">
            <label for="pseudo">Pseudo :</label>
            <input type="text" id="pseudo" name="pseudo" required>

            <label for="token">Token Discord :</label>
            <input type="text" id="token" name="token" required>

            <input type="submit" value="Ajouter">
        </form>

        <form method="post" action="/">
            <h2>Lancer le processus</h2>
            <input type="hidden" name="action" value="start_process">
            <label for="selected_user">Sélectionnez un utilisateur :</label>
            <select id="selected_user" name="selected_user" required>
                <option value="" disabled selected>-- Choisir un utilisateur --</option>
                {% for pseudo in users.keys() %}
                <option value="{{ pseudo }}">{{ pseudo }}</option>
                {% endfor %}
            </select>

            <label for="channel_id">ID du Canal :</label>
            <input type="text" id="channel_id" name="channel_id" required>

            <label for="threads">Nombre de Threads (1-5) :</label>
            <input type="number" id="threads" name="threads" min="1" max="5" required>

            <input type="submit" value="Démarrer">
        </form>
    </div>
</body>
</html>
"""

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

    return render_template_string(HTML_TEMPLATE, users=users)

if __name__ == '__main__':
    app.run(debug=True)
