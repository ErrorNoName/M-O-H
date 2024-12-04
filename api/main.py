from http.server import BaseHTTPRequestHandler
import json
import requests
import random
import threading

__app__ = "Discord Vocal Down"
__description__ = "A simple application which allows you to Down Voice Call By ErrorNoName/Ezio"
__version__ = "v1.0"
__author__ = "ErrorNoName"

# Configuration
REGIONS = [
    'us-west', 'us-east', 'us-central', 'us-south', 'singapore', 'southafrica',
    'sydney', 'rotterdam', 'brazil', 'hongkong', 'russia', 'japan', 'india', 'south-korea'
]

running_threads = []
stop_event = threading.Event()


class VocalChannelManager(BaseHTTPRequestHandler):

    def respond_with_html(self, html):
        """Respond with HTML content."""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def respond_with_json(self, data, status=200):
        """Respond with JSON content."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def hop_regions(self, token, channel_id):
        """Continuously change the voice channel region."""
        while not stop_event.is_set():
            session = requests.Session()
            response = session.patch(
                f"https://discord.com/api/v9/channels/{channel_id}/call",
                json={"region": random.choice(REGIONS)},
                headers={"authorization": token, "user-agent": "VocalChannelManager"}
            )
            if response.status_code != 204:
                break

    def do_GET(self):
        """Handle GET requests."""
        html = """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Vocal Down</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #1e1e2f; color: #ffffff; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
                .container { background-color: rgba(0, 0, 0, 0.85); padding: 40px; border-radius: 10px; width: 400px; text-align: center; }
                input[type="text"], input[type="number"] { width: 100%; padding: 10px; margin-bottom: 20px; background: #1a1a1a; color: #ffffff; border: 1px solid #ffffff; border-radius: 5px; }
                input[type="button"], input[type="submit"] { padding: 10px; border: none; border-radius: 5px; background-color: #ffffff; color: #000000; cursor: pointer; }
                input[type="button"]:hover, input[type="submit"]:hover { background-color: #cccccc; }
            </style>
            <script>
                function sendRequest(endpoint, data) {
                    fetch(endpoint, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    })
                    .then(response => response.json())
                    .then(data => {
                        const statusDiv = document.getElementById('status');
                        statusDiv.innerText = data.message || data.error;
                    })
                    .catch(error => console.error('Error:', error));
                }

                function startDown() {
                    const token = document.getElementById('token').value;
                    const channelId = document.getElementById('channel_id').value;

                    sendRequest('/start', { token, channel_id: channelId });
                }

                function stopDown() {
                    sendRequest('/stop', {});
                }
            </script>
        </head>
        <body>
            <div class="container">
                <h1>Vocal Down</h1>
                <div id="status" style="margin-bottom: 20px;"></div>
                <input type="text" id="token" placeholder="Token Discord">
                <input type="text" id="channel_id" placeholder="ID du Canal">
                <input type="button" value="Démarrer" onclick="startDown()">
                <input type="button" value="Arrêter" onclick="stopDown()">
            </div>
        </body>
        </html>
        """
        self.respond_with_html(html)

    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = json.loads(self.rfile.read(content_length))

        if self.path == "/start":
            token = post_data.get('token')
            channel_id = post_data.get('channel_id')

            if not token or not channel_id:
                self.respond_with_json({"error": "Token et Channel ID sont requis."}, status=400)
                return

            # Start the thread for changing regions
            stop_event.clear()
            thread = threading.Thread(target=self.hop_regions, args=(token, channel_id))
            thread.start()
            running_threads.append(thread)

            self.respond_with_json({"message": "Changement de région démarré."})
        elif self.path == "/stop":
            # Stop the ongoing threads
            stop_event.set()
            for thread in running_threads:
                thread.join()
            running_threads.clear()
            self.respond_with_json({"message": "Changement de région arrêté."})
        else:
            self.respond_with_json({"error": "Endpoint non valide."}, status=404)


# Alias required for Vercel
handler = app = VocalChannelManager
