from flask import Flask, render_template, request, jsonify
import threading
import requests
import random
import time
import sys

app = Flask(__name__)

__app__ = "Discord Vocal Down"
__description__ = "A simple application which allows you to Down Voice Call By ErrorNoName/Ezio"
__version__ = "v1.0"
__author__ = "ErrorNoName"

# Configuration
REGIONS = [
    'us-west', 'us-east', 'us-central', 'us-south', 'singapore', 'southafrica',
    'sydney', 'rotterdam', 'brazil', 'hongkong', 'russia', 'japan', 'india', 'south-korea'
]

# Variables globales pour gérer l'arrêt du script
stop_threads = False
thread_lock = threading.Lock()
current_thread = None

def hop_regions(token, channel_id):
    """Change the voice channel region in a loop."""
    global stop_threads
    session = requests.Session()

    while not stop_threads:
        try:
            response = session.patch(
                f"https://discord.com/api/v9/channels/{channel_id}/call",
                json={"region": random.choice(REGIONS)},
                headers={
                    "Authorization": token,
                    "User-Agent": "VocalChannelManager/1.0"
                }
            )
            if response.status_code == 204:
                print("Région changée avec succès.")
            else:
                print(f"Erreur lors du changement de région. Statut: {response.status_code}")
        except Exception as e:
            print(f"Exception lors du changement de région: {e}")
        
        # Attendre un certain temps avant de changer à nouveau la région
        # Par exemple, 60 secondes. Ajustez selon vos besoins.
        time.sleep(60)

@app.route('/')
def index():
    """Serve the frontend."""
    return render_template('index.html')

@app.route('/api/change_region', methods=['POST'])
def change_region():
    """Handle start and stop actions."""
    global stop_threads, current_thread

    data = request.get_json()
    action = data.get('action')
    token = data.get('token')
    channel_id = data.get('channel_id')

    if action not in ['start', 'stop']:
        return jsonify({"error": "Action invalide."}), 400

    if action == 'start':
        if not token or not channel_id:
            return jsonify({"error": "Token et Channel ID sont requis."}), 400

        with thread_lock:
            if current_thread and current_thread.is_alive():
                return jsonify({"error": "Le changement de région est déjà en cours."}), 400
            else:
                stop_threads = False
                current_thread = threading.Thread(target=hop_regions, args=(token, channel_id), daemon=True)
                current_thread.start()
                return jsonify({"message": "Le changement de région a commencé."}), 200

    elif action == 'stop':
        with thread_lock:
            if current_thread and current_thread.is_alive():
                stop_threads = True
                current_thread.join()
                return jsonify({"message": "Le changement de région a été arrêté."}), 200
            else:
                return jsonify({"error": "Le changement de région n'est pas en cours."}), 400

if __name__ == '__main__':
    # Vérifier si un port est passé en argument
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Port invalide. Utilisation du port 8080 par défaut.")
            port = 8080
    else:
        port = 8080

    app.run(host='0.0.0.0', port=port, debug=True)
