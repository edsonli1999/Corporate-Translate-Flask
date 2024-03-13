# Summary
- Takes in a user's phrase using a HTML form, transforms it using Google Gemini API to a corporate-appropriate phrase, and renders that back out
- Note: In instances where the user's prompts do not make sense, the server may time out and direct the user to a 504 Timeout Page. Though unpolished, this is expected behaviour and could be fixed by going back and re-entering a different phrase. 

## Tech Stack
- Framework: Python Flask
- APIs: Google Gemini API
- Deployed on: Vercel

# CLI Commands

## Running:
- To go into VENV: `venv\Scripts\activate`. To escape venv: `deactivate`
- To run flask app: `python app.py`

## Update dependencies in requirements.txt
- Go into venv
- Update current dependencies using `pip freeze > requirements.txt`
