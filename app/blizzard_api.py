import os
import requests
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_access_token():
  """
  Récupère un access token Blizzard avec les identifiants
  de l'application définis dans le fichier .env.

  Cette méthode utilise le Client Credentials Flow.
  """
  client_id = os.getenv("BLIZZARD_CLIENT_ID")
  client_secret = os.getenv("BLIZZARD_CLIENT_SECRET")
  region = os.getenv("BLIZZARD_REGION")

  url = f"https://{region}.battle.net/oauth/token"

  response = requests.post(
    url,
    auth=(client_id, client_secret),
    data={"grant_type": "client_credentials"}
  )

  response.raise_for_status()

  return response.json()["access_token"]

def get_character(realm, name):
  """
  Récupère les informations d'un personnage précis.

  Cette fonction correspond à notre premier prototype :
  on connaît le royaume et le nom du personnage.
  """

  token = get_access_token()

  region = os.getenv("BLIZZARD_REGION")

  url = (
    f"https://{region}.api.blizzard.com/"
    f"profile/wow/character/{realm.lower()}/{name.lower()}"
  )

  headers = {
    "Authorization": f"Bearer {token}",
    "Battlenet-Namespace": f"profile-{region}"
  }

  params = {"locale": "fr_FR"}

  response = requests.get(
    url,
    headers=headers,
    params=params
  )

  response.raise_for_status()

  return response.json()

def get_user_profile(access_token):
  """
  Récupère le profil WoW du compte Battle.net connecté.

  Contrairement à get_character(), cette fonction ne demande
  pas de royaume ni de nom de personnage.

  Blizzard utilise le access_token obtenu avec OAuth pour
  déterminer quel compte WoW est connecté.
  """
  # Le token OAuth est envoyé à Blizzard pour authentifier la requête.
  headers = {
    "Authorization": f"Bearer {access_token}"
  }

  # Le namespace "profile-eu" indique que nous travaillons avec
  # les données de profil de la région européenne.
  params = {
    "namespace": "profile-eu",
    "locale": "en_GB"
  }

  # Endpoint permettant de récupérer le profil WoW du compte
  # actuellement connecté.
  response = requests.get(
    "https://eu.api.blizzard.com/profile/user/wow",
    headers=headers,
    params=params
  )

  # Affichage temporaire pour vérifier la réponse de Blizzard.
  # Je supprimerai ces prints lorsque le prototype sera terminé.
  print("PROFILE STATUS:", response.status_code)
  print("PROFILE DATA:", response.text)

  # Si Blizzard répond correctement, on transforme le JSON
  # en dictionnaire Python et on le retourne.
  if response.status_code == 200:
    return response.json()

  # En cas d'erreur, on retourne None.
  return None

def get_user_characters(access_token):
  """
  Récupère la liste des personnages du compte WoW connecté.

  Cette fonction utilise get_user_profile() pour récupérer
  le profil complet du compte, puis extrait directement
  les personnages présents dans "wow_accounts".
  """

  # Récupération du profil complet depuis Blizzard.
  profile = get_user_profile(access_token)

  # Si le profil n'a pas pu être récupéré,
  # on retourne une liste vide.
  if not profile:
    return []

  # Un compte Battle.net peut contenir plusieurs comptes WoW.
  wow_accounts = profile.get("wow_accounts", [])

  # Liste qui contiendra tous les personnages.
  characters = []

  # Parcours des comptes WoW.
  for wow_account in wow_accounts:

    # Récupération de la liste des personnages
    # appartenant à ce compte WoW.
    account_characters = wow_account.get("characters", [])

    # Chaque élément contient directement les informations
    # du personnage : name, id, realm, level, etc.
    for character in account_characters:

      # On ajoute directement l'objet character complet.
      characters.append(character)

  # Retourne la liste complète des personnages.
  return characters

def get_character_media(access_token, realm_slug, character_name):
  """
  Récupère les médias (images) d'un personnage précis.

  Pour notre test, nous allons utiliser cette fonction
  avec un seul personnage avant de l'intégrer à toute
  notre liste de personnages.
  """

  # Région utilisée par notre application.
  region = os.getenv("BLIZZARD_REGION")

  # URL de l'endpoint Character Media.
  url = (
    f"https://{region}.api.blizzard.com/"
    f"profile/wow/character/"
    f"{realm_slug.lower()}/"
    f"{character_name.lower()}/"
    f"character-media"
  )

  # Le token utilisateur obtenu avec OAuth permet
  # d'accéder aux données de profil du personnage.
  headers = {
    "Authorization": f"Bearer {access_token}"
  }

  # Namespace et langue nécessaires pour l'API.
  params = {
    "namespace": f"profile-{region}",
    "locale": "en_GB"
  }

  # Appel de l'API Blizzard.
  response = requests.get(
    url,
    headers=headers,
    params=params
  )

  # Affichage temporaire pour voir exactement
  # ce que Blizzard nous retourne.
  print("MEDIA STATUS:", response.status_code)
  print("MEDIA DATA:", response.text)

  # Si la requête fonctionne, on retourne le JSON.
  if response.status_code == 200:

    # On transforme le JSON en dictionnaire Python.
    data = response.json()

    # Recherche de l'avatar dans les médias disponibles.
    for asset in data.get("assets", []):
      if asset.get("key") == "avatar":
        return asset.get("value")

    # Aucun avatar trouvé, on retourne None.
    return None

  # En cas d'erreur, on retourne None.
  return None

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/character/<realm>/<name>")
def character(realm, name):
  try:
    data = get_character(realm, name)

    return render_template(
      "character.html",
      character=data
    )

  except Exception as e:
    return f"Erreur : {str(e)}"

if __name__ == "__main__":
  app.run(debug=True)
