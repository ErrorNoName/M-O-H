from http.server import BaseHTTPRequestHandler
import json
import requests
import random
import threading

__app__ = "Discord Vocal Down"
__description__ = "A simple application which allows you to Down Voice Call By ErrorNoName/Ezio"
__version__ = "v1.0"
__author__ = "ErrorNoName"

REGIONS = [
    'us-west', 'us-east', 'us-central', 'us-south', 'singapore', 'southafrica',
    'sydney', 'rotterdam', 'brazil', 'hongkong', 'russia', 'japan', 'india', 'south-korea'
]

running_threads = []
stop_event = threading.Event()

class VocalChannelManager(BaseHTTPRequestHandler):

    def respond_with_html(self, html):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def respond_with_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def hop_regions(self, token, channel_id):
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
        html = """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Vocal Down</title>
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

                    sendRequest('/api/main/start', { token, channel_id: channelId });
                }

                function stopDown() {
                    sendRequest('/api/main/stop', {});
                }
            </script>
        </head>
        <body>
            <div id="status"></div>
            <input type="text" id="token" placeholder="Token Discord">
            <input type="text" id="channel_id" placeholder="ID du Canal">
            <button onclick="startDown()">Démarrer</button>
            <button onclick="stopDown()">Arrêter</button>
        </body>
        </html>
        """
        self.respond_with_html(html)

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = json.loads(self.rfile.read(content_length))

        if self.path == "/api/main/start":
            token = post_data.get('token')
            channel_id = post_data.get('channel_id')

            if not token or not channel_id:
                self.respond_with_json({"error": "Token et Channel ID sont requis."}, status=400)
                return

            stop_event.clear()
            thread = threading.Thread(target=self.hop_regions, args=(token, channel_id))
            thread.start()
            running_threads.append(thread)

            self.respond_with_json({"message": "Changement de région démarré."})
        elif self.path == "/api/main/stop":
            stop_event.set()
            for thread in running_threads:
                thread.join()
            running_threads.clear()
            self.respond_with_json({"message": "Changement de région arrêté."})
        else:
            self.respond_with_json({"error": "Endpoint non valide."}, status=404)

# Alias required for Vercel
handler = app = VocalChannelManager
