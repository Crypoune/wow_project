import os
import requests
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_access_token():
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
  token = get_access_token()
  region = os.getenv("BLIZZARD_REGION")

  url = f"https://{region}.api.blizzard.com/profile/wow/character/{realm.lower()}/{name.lower()}"
  headers = {
    "Authorization": f"Bearer {token}",
    "Battlenet-Namespace": f"profile-{region}"
  }
  params = {"locale": "fr_FR"}

  response = requests.get(url, headers=headers, params=params)
  response.raise_for_status()
  return response.json()

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/character/<realm>/<name>")
def character(realm, name):
  try:
    data = get_character(realm, name)
    return render_template("character.html", character=data)
  except Exception as e:
    return f"Erreur : {str(e)}"
  
if __name__ == "__main__":
  app.run(debug=True)