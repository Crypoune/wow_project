import os
import secrets
import requests

from flask import Blueprint, redirect, render_template, request, session
from urllib.parse import urlencode
from dotenv import load_dotenv

from .blizzard_api import (
  get_user_characters,
  get_character_media
)

load_dotenv()

main = Blueprint('main', __name__)

@main.route('/login')
def login():
  state = secrets.token_urlsafe(16)
  session['oauth_state'] = state

  base_url = "https://oauth.battle.net/authorize"

  params = {
    "client_id": os.getenv("BLIZZARD_CLIENT_ID"),
    "response_type": "code",
    "redirect_uri": os.getenv("BLIZZARD_REDIRECT_URI"),
    "scope": "wow.profile",
    "state": state
  }

  auth_url = f"{base_url}?{urlencode(params)}"
  print("AUTH URL:", auth_url)

  return redirect(auth_url)

@main.route('/callback')
def callback():

  # Récupération du code et du state envoyés par Battle.net
  # après l'autorisation de l'utilisateur.
  code = request.args.get('code')
  state = request.args.get('state')

  # Vérification de sécurité du state OAuth.
  if not state or state != session.get('oauth_state'):
    return "Invalid OAuth state", 400

  # Vérification de la présence du authorization code.
  if not code:
    return "No authorization code", 400

  # URL utilisée pour échanger le authorization code
  # contre un access token.
  token_url = "https://oauth.battle.net/token"

  data = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": os.getenv("BLIZZARD_REDIRECT_URI")
  }

  # Demande d'un access token à Blizzard.
  response = requests.post(
    token_url,
    data=data,
    auth=(
      os.getenv("BLIZZARD_CLIENT_ID"),
      os.getenv("BLIZZARD_CLIENT_SECRET")
    )
  )

  # Vérification de la réponse de Blizzard.
  if response.status_code != 200:
    return f"Token request failed: {response.text}", 400

  # Récupération des données du token.
  token_data = response.json()
  access_token = token_data.get("access_token")

  # Vérification temporaire de la récupération du token.
  # On affiche uniquement sa longueur et jamais sa valeur.
  print(
    "ACCESS TOKEN RECEIVED:",
    len(access_token)
  )

  # Récupération de la liste des personnages.
  characters = get_user_characters(access_token)

  # récupération du portrait d'un personnage.
  for character in characters:

    # Récupération du slug du royaume.
    # Exemple : "Varimathras" devient "varimathras".
    realm_slug = character["realm"]["slug"]

    # Récupération du nom du personnage.
    character_name = character["name"]

    # Demande à Blizzard l'avatar de ce personnage.
    avatar_url = get_character_media(
      access_token,
      realm_slug,
      character_name
    )

    # Ajout de l'URL du portrait dans les données du personnage.
    character["avatar_url"] = avatar_url

    # Affichage temporaire pour suivre la progression.
    print(
      "AVATAR",
      character_name,
      "-",
      realm_slug,
      "-",
      avatar_url
    )

  # Affichage temporaire du nombre de personnages récupérés.
  print("CHARACTERS FOUND:", len(characters))

  # Affiche la structure du premier élément pour vérifier
  # exactement ce que notre fonction retourne.
  print("FIRST CHARACTER:", characters[0])

  # Affiche le nombre de personnages récupérés.
  print("CHARACTERS FOUND:", len(characters))

  return render_template(
    "characters.html",
    characters=characters
  )
