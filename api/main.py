import json
import requests
import random
import threading

# Configuration
REGIONS = [
    'us-west', 'us-east', 'us-central', 'us-south', 'singapore', 'southafrica',
    'sydney', 'rotterdam', 'brazil', 'hongkong', 'russia', 'japan', 'india', 'south-korea'
]

# Variable globale pour gérer l'arrêt du script
stop_threads = False

def hop_regions(token, channel_id):
    """Change the voice channel region in a loop."""
    global stop_threads
    session = requests.Session()

    while not stop_threads:
        response = session.patch(
            f"https://discord.com/api/v9/channels/{channel_id}/call",
            json={"region": random.choice(REGIONS)},
            headers={"authorization": token, "user-agent": "VocalChannelManager"}
        )
        if response.status_code == 204:
            print("Région changée avec succès.")
        else:
            print("Erreur lors du changement de région.")

def handler(event, context):
    """Handler for Vercel requests."""
    global stop_threads

    # Vérifie la méthode de la requête
    method = event["httpMethod"]
    if method == "GET":
        # Retourne le HTML
        html = """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Vocal Down</title>
            <style>
                /* Styles simplifiés */
                body {
                    font-family: Arial, sans-serif;
                    background-color: #000000;
                    color: #ffffff;
                    text-align: center;
                    padding: 20px;
                }
                input, button {
                    margin: 10px;
                    padding: 10px;
                }
            </style>
            <script>
                function sendRequest(action) {
                    const token = document.getElementById("token").value;
                    const channel_id = document.getElementById("channel_id").value;
                    fetch("/", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ action, token, channel_id })
                    })
                    .then(response => response.json())
                    .then(data => alert(data.message || data.error))
                    .catch(err => alert("Erreur de communication avec le serveur."));
                }
            </script>
        </head>
        <body>
            <h1>Vocal Down</h1>
            <label>Token Discord:</label>
            <input type="text" id="token"><br>
            <label>ID du Canal:</label>
            <input type="text" id="channel_id"><br>
            <button onclick="sendRequest('start')">Changer la région</button>
            <button onclick="sendRequest('stop')">Arrêter</button>
        </body>
        </html>
        """
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": html
        }

    elif method == "POST":
        # Traite les requêtes POST
        body = json.loads(event["body"])
        action = body.get("action")
        token = body.get("token")
        channel_id = body.get("channel_id")

        if action == "start":
            if not token or not channel_id:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Token et Channel ID sont requis."})
                }
            stop_threads = False
            threading.Thread(target=hop_regions, args=(token, channel_id), daemon=True).start()
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Le changement de région a commencé."})
            }

        elif action == "stop":
            stop_threads = True
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "Le changement de région a été arrêté."})
            }

        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Action invalide."})
        }

    return {
        "statusCode": 405,
        "body": json.dumps({"error": "Méthode non autorisée."})
    }
