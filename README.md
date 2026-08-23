# WoW Character Tracker

## Current Status

🚧 Prototype / V0

The first functional version of the project is now working.

The current version focuses on retrieving and displaying World of Warcraft characters through the Blizzard API.

The architecture and technology choices may evolve as the project progresses.

---

## Project Overview

This is a personal learning project built to explore Python web development and the Blizzard World of Warcraft API.

The application connects to a Battle.net account through Blizzard OAuth and retrieves the World of Warcraft characters associated with the account.

The current prototype displays the characters through a simple web interface, including their portraits, level, realm, class, race, and faction.

---

## Current Features

- Battle.net OAuth authentication
- Retrieval of the user's World of Warcraft profile
- Retrieval of World of Warcraft characters
- Character level
- Character realm
- Character class
- Character race
- Character faction
- Character portraits through the Blizzard Character Media API
- Alliance and Horde icons
- World of Warcraft class colors
- Responsive character grid
- Visual distinction between max-level and leveling characters

---

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Jinja2
- **API:** Blizzard World of Warcraft API
- **Authentication:** Blizzard OAuth 2.0
- **Environment variables:** python-dotenv
- **HTTP requests:** Requests
- **Version control:** Git / GitHub

---

## Project Structure

```text
wow_project/
├── app/
│   ├── static/
│   │   ├── images/
│   │   │   ├── alliance.png
│   │   │   └── horde.png
│   │   └── style.css
│   │
│   ├── templates/
│   │   ├── characters.html
│   │   └── index.html
│   │
│   ├── blizzard_api.py
│   └── routes.py
│
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

---

## How It Works

The application follows this basic flow:

```text
User
  ↓
Battle.net OAuth
  ↓
Access Token
  ↓
Blizzard WoW Profile API
  ↓
Character List
  ↓
Character Media API
  ↓
Flask / Jinja2
  ↓
HTML / CSS
```

The character data is retrieved dynamically from Blizzard when the user logs in.

Character portraits are retrieved through Blizzard's Character Media endpoint.

---

## Setup

1. Clone the repository

git clone <repository-url>
cd wow_project

2. Create a virtual environment

python -m venv venv

(Activate it:)

- Windows:
  venv\Scripts\activate

- macOS / Linux:
  source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Configure environment variables

Create a .env file locally at the root of the project:
BLIZZARD_CLIENT_ID=your_client_id
BLIZZARD_CLIENT_SECRET=your_client_secret
BLIZZARD_REGION=eu
BLIZZARD_REDIRECT_URI=http://127.0.0.1:5000/callback

The Blizzard OAuth application must use the same redirect URI.

5. Run the application

python run.py

Then open:

http://127.0.0.1:5000/login

The application will redirect you to Battle.net for authentication.

---

## Learning Objectives

- Practice Python and Flask
- Understand OAuth 2.0 authentication
- Work with REST APIs
- Learn how to consume Blizzard's World of Warcraft API
- Handle JSON data returned by an external API
- Connect a Python backend with HTML templates
- Practice responsive CSS
- Understand the basics of API-driven web applications
- Apply Git and GitHub best practices

---

## Future Features

Possible future improvements include:

- Character detail pages
- Character search and filtering
- More character information
- Item level and equipment
- Mythic+ progression
- Raid progression
- Achievements
- Data persistence with a database
- User accounts
- Improved UI/UX
- Frontend framework integration
- Caching and API request optimization
- Further exploration of the Blizzard API

---

## Disclaimer

World of Warcraft and Blizzard Entertainment are trademarks or registered trademarks of Blizzard Entertainment, Inc.

This project is an independent educational project and is not affiliated with or endorsed by Blizzard Entertainment.
