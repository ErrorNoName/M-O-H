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
                /* Animation de fond fade subtil */
                @keyframes backgroundFade {
                    0% { background-color: #000000; }
                    50% { background-color: #1a1a1a; }
                    100% { background-color: #000000; }
                }

                /* Effet typewriter pour le titre */
                @keyframes typewriter {
                    from { width: 0; }
                    to { width: 22ch; }
                }

                @keyframes blink {
                    50% { border-color: transparent; }
                }

                /* Thème sombre global */
                body {
                    margin: 0;
                    padding: 0;
                    background: #000000;
                    color: #ffffff;
                    font-family: 'Courier New', Courier, monospace;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    overflow: hidden;
                    animation: backgroundFade 20s infinite;
                }

                /* Menu de navigation */
                .menu {
                    position: absolute;
                    top: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    display: flex;
                    gap: 30px;
                }

                .menu a {
                    color: #ffffff;
                    text-decoration: none;
                    font-size: 18px;
                    position: relative;
                    padding: 5px 0;
                    transition: color 0.3s;
                }

                .menu a::after {
                    content: '';
                    position: absolute;
                    width: 0;
                    height: 2px;
                    background: #ffffff;
                    left: 0;
                    bottom: -5px;
                    transition: width 0.3s;
                }

                .menu a:hover::after {
                    width: 100%;
                }

                .menu a:hover {
                    color: #cccccc;
                }

                /* Conteneur principal */
                .container {
                    background-color: rgba(0, 0, 0, 0.85);
                    padding: 40px 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
                    width: 400px;
                    text-align: center;
                    position: relative;
                    z-index: 1;
                }

                /* Logo avec effet personnalisé */
                .logo {
                    width: 150px;
                    height: 150px;
                    margin: 0 auto 20px;
                    background: url('https://i.ibb.co/dMK3t7j/4328d00292b082b5f8fa1b648d25b666-removebg-preview.png') no-repeat center center / contain;
                    position: relative;
                }

                /* Effet de lueur autour du logo suivant la forme */
                .logo::after {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(255, 255, 255, 0.2);
                    filter: blur(20px);
                    border-radius: 10px; /* Ajuster selon la forme du logo */
                    animation: pulse 3s infinite;
                }

                /* Animation de pulsation */
                @keyframes pulse {
                    0% { opacity: 0.6; transform: scale(1); }
                    50% { opacity: 1; transform: scale(1.05); }
                    100% { opacity: 0.6; transform: scale(1); }
                }

                /* Titre avec effet typewriter */
                h1 {
                    font-size: 24px;
                    margin-bottom: 30px;
                    overflow: hidden;
                    border-right: 2px solid #ffffff;
                    white-space: nowrap;
                    margin: 0 auto 20px;
                    letter-spacing: 2px;
                    animation: typewriter 4s steps(22) 1s forwards, blink 0.75s step-end infinite;
                    width: 0;
                }

                /* Formulaire */
                form {
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                }

                label {
                    text-align: left;
                    font-size: 14px;
                    margin-bottom: 5px;
                }

                input[type="text"], input[type="number"] {
                    padding: 10px;
                    border: 1px solid #ffffff;
                    border-radius: 5px;
                    background-color: #1a1a1a;
                    color: #ffffff;
                    font-size: 16px;
                    transition: border 0.3s, background-color 0.3s;
                }

                input[type="text"]:focus, input[type="number"]:focus {
                    border: 2px solid #ffffff;
                    outline: none;
                    background-color: #333333;
                }

                input[type="submit"] {
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                    background-color: #ffffff;
                    color: #000000;
                    font-size: 16px;
                    cursor: pointer;
                    transition: background-color 0.3s, transform 0.3s;
                }

                input[type="submit"]:hover {
                    background-color: #e0e0e0;
                    transform: scale(1.05);
                }

                /* Footer */
                .footer {
                    position: absolute;
                    bottom: 10px;
                    width: 100%;
                    text-align: center;
                    font-size: 12px;
                    color: #ffffff;
                }

                .footer a {
                    color: #ffffff;
                    text-decoration: underline;
                }

                /* Réactivité */
                @media (max-width: 500px) {
                    .container {
                        width: 90%;
                        padding: 30px 20px;
                    }

                    .menu {
                        flex-direction: column;
                        gap: 15px;
                    }

                    .logo {
                        width: 120px;
                        height: 120px;
                    }

                    h1 {
                        font-size: 20px;
                    }
                }
            </style>
        </head>
        <body>
            <!-- Menu de navigation -->
            <div class="menu">
                <a href="#">Accueil</a>
                <a href="#">Fonctionnalités</a>
                <a href="#">Contact</a>
            </div>

            <!-- Conteneur principal -->
            <div class="container">
                <div class="logo"></div>
                <h1>Vocal Down</h1>
                <form method="post">
                    <label for="token">Token Discord :</label>
                    <input type="text" id="token" name="token" required>

                    <label for="channel_id">ID du Canal :</label>
                    <input type="text" id="channel_id" name="channel_id" required>

                    <input type="submit" value="Changer la région">
                </form>
            </div>

            <!-- Footer -->
            <div class="footer">
                Created by Ezio/ErrorNoName | <a href="https://discord.com/users/830858630315376730" target="_blank">Contact</a>
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
