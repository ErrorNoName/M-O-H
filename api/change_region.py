# api/change_region.py

import json
import requests
import random

REGIONS = [
    'us-west', 'us-east', 'us-central', 'us-south', 'singapore', 'southafrica',
    'sydney', 'rotterdam', 'brazil', 'hongkong', 'russia', 'japan', 'india', 'south-korea'
]

def handler(request, context):
    if request.method == 'POST':
        try:
            data = request.json
            token = data.get('token')
            channel_id = data.get('channel_id')

            if not token or not channel_id:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Token et Channel ID sont requis."})
                }

            region = random.choice(REGIONS)
            headers = {
                "Authorization": token,
                "User-Agent": "VocalDown"
            }
            response = requests.patch(
                f"https://discord.com/api/v9/channels/{channel_id}/call",
                json={"region": region},
                headers=headers
            )

            if response.status_code == 204:
                return {
                    "statusCode": 200,
                    "body": json.dumps({"message": f"La région a été changée avec succès en {region}."})
                }
            else:
                return {
                    "statusCode": 500,
                    "body": json.dumps({"error": "Échec lors du changement de région."})
                }

        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }
    else:
        return {
            "statusCode": 405,
            "body": json.dumps({"error": "Méthode non autorisée."})
        }
