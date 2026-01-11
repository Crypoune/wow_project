import os
import secrets
import requests
from flask import Blueprint, redirect, request, session
from urllib.parse import urlencode
from dotenv import load_dotenv

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
  code = request.args.get('code')
  state = request.args.get('state')

  if not state or state != session.get('oauth_state'):
    return "Invalid OAuth state", 400

  if not code:
    return "No authorization code", 400
      
  token_url = "https://oauth.battle.net/token"

  data = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": os.getenv("BLIZZARD_REDIRECT_URI")
  }

  response = requests.post(
    token_url,
    data=data,
    auth=(
      os.getenv("BLIZZARD_CLIENT_ID"),
      os.getenv("BLIZZARD_CLIENT_SECRET")
    )
  )

  if response.status_code != 200:
    return f"Token request failed: {response.text}", 400
      
  token_data = response.json()
  access_token = token_data.get("access_token")

  return f"Login successful 🎉<br>Access token received (length: {len(access_token)})"