import sys
import threading
from PyQt5.QtCore import QUrl, Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
import subprocess
import time
import socket

# Fonction pour démarrer le serveur Flask avec un port spécifique
def start_flask(port):
    subprocess.call(['python', 'app.py', str(port)])

# Classe principale de l'application
class MainWindow(QMainWindow):
    def __init__(self, port):
        super().__init__()
        self.setWindowTitle("Vocal Down")  # Titre personnalisé
        self.setWindowFlags(Qt.FramelessWindowHint)  # Enlever la bordure
        self.setGeometry(100, 100, 1200, 800)  # Position et taille de la fenêtre

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(f"http://localhost:{port}/"))
        self.setCentralWidget(self.browser)

        self.oldPos = self.pos()  # Stocke la position initiale de la fenêtre

    def mousePressEvent(self, event):
        """Capture l'événement lorsque le bouton gauche de la souris est pressé."""
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()  # Enregistre la position globale de la souris
            event.accept()

    def mouseMoveEvent(self, event):
        """Déplace la fenêtre lorsque la souris est déplacée avec le bouton gauche maintenu."""
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.oldPos  # Calcule la différence de position
            self.move(self.x() + delta.x(), self.y() + delta.y())  # Déplace la fenêtre
            self.oldPos = event.globalPos()  # Met à jour la position initiale
            event.accept()


def find_free_port():
    """Trouver un port libre."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

if __name__ == '__main__':
    # Port par défaut
    port = 8080
    try:
        # Vérifier si le port 8080 est disponible
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', port))
    except socket.error:
        print(f"Port {port} est déjà utilisé. Recherche d'un port libre...")
        port = find_free_port()
        print(f"Utilisation du port {port}.")

    # Démarrer le serveur Flask dans un thread séparé
    flask_thread = threading.Thread(target=start_flask, args=(port,), daemon=True)
    flask_thread.start()

    # Attendre un peu pour s'assurer que Flask démarre
    time.sleep(5)

    # Lancer l'application PyQt
    app = QApplication(sys.argv)
    window = MainWindow(port)
    window.show()
    sys.exit(app.exec_())
