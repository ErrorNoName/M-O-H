from http.server import BaseHTTPRequestHandler
import json
import requests
import random

__app__ = "Discord Vocal Down"
__description__ = "A simple application which allows you to Down Voice Call By ErrorNoName/Ezio"
__version__ = "v1.0"
__author__ = "ErrorNoName"

# Configuration
REGIONS = [
    'us-west', 'us-east', 'us-central', 'us-south', 'singapore', 'southafrica',
    'sydney', 'rotterdam', 'brazil', 'hongkong', 'russia', 'japan', 'india', 'south-korea'
]

class VocalChannelManager(BaseHTTPRequestHandler):

    def respond_with_html(self, html):
        """Respond with HTML content."""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def hop_regions(self, token, channel_id):
        """Change the voice channel region."""
        session = requests.Session()
        response = session.patch(
            f"https://discord.com/api/v9/channels/{channel_id}/call",
            json={"region": random.choice(REGIONS)},
            headers={"authorization": token, "user-agent": "VocalChannelManager"}
        )
        return response.status_code

    def do_GET(self):
        """Handle GET requests."""
        html = """
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
                <form method="post">
                    <label for="token">Token Discord :</label>
                    <input type="text" id="token" name="token" required>

                    <label for="channel_id">ID du Canal :</label>
                    <input type="text" id="channel_id" name="channel_id" required>

                    <input type="submit" value="Changer la région">
                </form>
            </div>
        </body>
        </html>
        """
        self.respond_with_html(html)

    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = dict(x.split('=') for x in post_data.split('&'))

        token = data.get('token')
        channel_id = data.get('channel_id')

        if not token or not channel_id:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Token et Channel ID sont requis."}).encode())
            return

        # Change region
        status_code = self.hop_regions(token, channel_id)
        if status_code == 204:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "La région a été changée avec succès."}).encode())
        else:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Échec lors du changement de région."}).encode())

# Alias required for Vercel
handler = app = VocalChannelManager
