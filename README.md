# Discord Vocal Down 🎙️

![License](https://img.shields.io/github/license/ErrorNoName/M-O-H?style=flat-square)
![Version](https://img.shields.io/badge/version-1.0-blue?style=flat-square)
![Framework](https://img.shields.io/badge/framework-Flask-orange?style=flat-square)

**Discord Vocal Down** est une application web simple mais puissante qui permet de **changer automatiquement la région des appels vocaux sur Discord**. Ce projet, développé par **Ezio/ErrorNoName**, est conçu pour perturber temporairement les appels vocaux en utilisant une boucle de changement de région.

---

## 📋 Fonctionnalités

- **Gestion des régions vocales Discord :**
  - Boucle de changement de région parmi une liste de régions Discord préconfigurées.
  - Fonctionnement en temps réel via un backend Flask.
- **Interface utilisateur moderne :**
  - Design sombre et épuré.
  - Animations fluides et interface intuitive.
- **Actions principales :**
  - **Démarrer** : Lance la boucle de changement de région.
  - **Arrêter** : Met fin à la boucle en toute sécurité.
- **Backend robuste :**
  - Utilisation de threads pour gérer les actions de démarrage/arrêt.
  - Validation des entrées utilisateur (token et ID de canal).

---

## 🚀 Installation et Configuration

### Prérequis

- **Python 3.8 ou supérieur**
- **pip** (gestionnaire de paquets Python)
- Navigateurs modernes (pour l'interface utilisateur)

### Installation

1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/ErrorNoName/M-O-H.git
   cd M-O-H
   ```

2. **Installez les dépendances** :
   ```bash
   source create_venv.sh
   ```

3. **Lancez l'application** :
   ```bash
   python Interface.py
   ```

4. **Accédez à l'interface utilisateur** :
   - Ouvrez votre navigateur et rendez-vous sur [http://localhost:8080](http://localhost:8080).

---

## 📂 Structure du Projet

```
Discord-Vocal-Down/
├── app.py              # Backend Flask
├── templates/
│   └── index.html      # Frontend de l'application
└── requirements.txt    # Liste des dépendances
```

---

## 🛠️ Utilisation

1. **Lancez le script** (`python app.py`) pour démarrer le serveur Flask.
2. **Accédez à l'interface utilisateur** dans votre navigateur.
3. **Entrez vos informations** :
   - **Token Discord** : Votre token d'utilisateur Discord.
   - **ID du Canal** : L'identifiant du canal vocal à perturber.
4. **Cliquez sur "Changer la région"** pour démarrer la boucle.
5. **Cliquez sur "Arrêter"** pour stopper la boucle.

---

## 🌟 Fonctionnalités Avancées

### Liste des Régions Discord

Les régions vocales disponibles sont :
- `us-west`, `us-east`, `us-central`, `us-south`
- `singapore`, `southafrica`, `sydney`
- `rotterdam`, `brazil`, `hongkong`
- `russia`, `japan`, `india`, `south-korea`

### Backend Flask

- **Endpoints** :
  - `/` : Charge l'interface utilisateur.
  - `/api/change_region` : Gère les actions de démarrage/arrêt de la boucle.

### Frontend avec Thème Sombre

- Animations CSS avancées (effet `typewriter`, pulsation du logo, transitions fluides).
- Conception adaptative pour les écrans mobiles.

---

## ⚠️ Avertissements

- **Respect des Conditions Discord** : Cet outil est destiné à des fins éducatives et de test uniquement. L'utilisation abusive de cette application peut entraîner la suspension de votre compte Discord.
- **Données sensibles** : Ne partagez jamais votre token Discord.

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Si vous avez des suggestions ou souhaitez signaler un problème :

1. **Forkez le dépôt**.
2. **Créez une branche** : `git checkout -b feature-nom-de-la-feature`.
3. **Commitez vos modifications** : `git commit -m "Ajout d'une fonctionnalité."`
4. **Poussez votre branche** : `git push origin feature-nom-de-la-feature`.
5. **Soumettez une Pull Request**.

---

## 📜 Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](https://github.com/ErrorNoName/Discord-Vocal-Down/blob/main/LICENSE) pour plus d'informations.

---

## 📧 Contact

Pour toute question ou assistance, contactez-moi via :
- [**Discord**](https://discord.com/users/830858630315376730)
- [**GitHub**](https://github.com/ErrorNoName)

---

_"Créer, tester, innover."_ - **Ezio/ErrorNoName**
