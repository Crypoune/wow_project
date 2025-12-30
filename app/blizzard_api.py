import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("BLIZZARD_CLIENT_ID")
CLIENT_SECRET = os.getenv("BLIZZARD_CLIENT_SECRET")

def get_access_token():
    url = "https://oauth.battle.net/token"
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    response.raise_for_status()
    return response.json()["access_token"]

def get_eu_realms():
    token = get_access_token()
    url = "https://eu.api.blizzard.com/data/wow/realm/index?namespace=dynamic-eu&locale=fr_FR&access_token=" + token
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # retourne un dictionnaire {nom: slug}
    return {r['name'].lower(): r['slug'] for r in data['realms']}

def get_character_profile(realm_name, character_name):
    token = get_access_token()
    
    # vérifier le slug du royaume
    realms = get_eu_realms()
    realm_slug = realms.get(realm_name.lower())
    if not realm_slug:
        raise ValueError(f"Realm '{realm_name}' non trouvé. Vérifie le nom exact.")
    
    url = f"https://eu.api.blizzard.com/profile/wow/character/{realm_slug}/{character_name.lower()}?namespace=profile-eu&locale=fr_FR&access_token={token}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    realm_name = "Dalaran"
    character_name = "Crypoune"

    data = get_character_profile(realm_name, character_name)
    
    print(f"Name: {data.get('name')}")
    print(f"Level: {data.get('level')}")
    print(f"Race: {data.get('race', {}).get('name')}")
    print(f"Class: {data.get('character_class', {}).get('name')}")
