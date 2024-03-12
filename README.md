# Summary
- Takes in a user's phrase using a HTML form, transforms it using OpenAI API to a corporate-appropriate phrase, and renders that back out

## Tech Stack
- Framework: Python Flask
- APIs: OpenAI API
- Deployed on: Vercel

# CLI Commands

## Running:
- To go into VENV: `venv\Scripts\activate`. To escape venv: `deactivate`
- To run flask app: `python app.py`


## Initial Set up:
- To set up Virtual ENV: `python -m venv venv`
- Go into VENV
- Installing flask and required packages: 
```
pip install Flask openai
pip install python-dotenv
```

## Update dependencies in requirements.txt
- Go into venv
- Pushing current dependencies using `pip freeze > requirements.txt`
