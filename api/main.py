import json
import random
import requests

# Liste des régions disponibles
REGIONS = ['us-west', 'us-east', 'us-central', 'us-south', 'singapore', 'southafrica',
           'sydney', 'rotterdam', 'brazil', 'hongkong', 'russia', 'japan', 'india', 'south-korea']

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
        input[type="text"], input[type="number"] {
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
        <form method="post" action="/api/main">
            <label for="token">Token Discord :</label>
            <input type="text" id="token" name="token" required>

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

def hop_regions(token, channel_id):
    """
    Change la région d'un salon vocal de manière aléatoire.
    """
    session = requests.Session()
    response = session.patch(
        f"https://discord.com/api/v9/channels/{channel_id}/call",
        json={"region": random.choice(REGIONS)},
        headers={"authorization": token, "user-agent": "9e1 Crasher"}
    )
    return response.status_code

def handler(event, context):
    """
    Fonction principale appelée par Vercel.
    """
    if event['httpMethod'] == 'GET':
        # Renvoyer la page HTML
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": HTML_TEMPLATE
        }

    elif event['httpMethod'] == 'POST':
        # Parse les données envoyées
        body = json.loads(event['body'])
        token = body.get('token')
        channel_id = body.get('channel_id')

        if not token or not channel_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Token et Channel ID sont requis."})
            }

        # Tenter de changer la région
        status_code = hop_regions(token, channel_id)
        if status_code == 204:
            return {
                "statusCode": 200,
                "body": json.dumps({"message": "La région a été changée avec succès."})
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Échec lors du changement de région."})
            }

    return {
        "statusCode": 405,
        "body": json.dumps({"error": "Méthode non autorisée."})
    }
