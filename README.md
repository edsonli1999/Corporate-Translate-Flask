# Summary
- Takes in a user's phrase using a HTML form, transforms it using Google Gemini API to a corporate-appropriate phrase, and renders that back out
- Note: In instances where the user's prompts do not make sense, the server may time out and direct the user to a 504 Timeout Page. Though unpolished, this is expected behaviour and could be fixed by going back and re-entering a different phrase. 

## Tech Stack
- Framework: Python Flask
- APIs: Google Gemini API
- Deployed on: Vercel

## Notable features:
- Dark mode
- Works on mobile (mainly portrait, landscape is still not very usable)

# CLI Commands

## Running a local server:
- To go into VENV: `venv\Scripts\activate`. To escape venv: `deactivate`
- To run flask app: `python app.py`

## First time (if no venv folder exits)
- Create a new venv: `python -m venv venv`
- activate venv: `venv/scripts/acivate`
- Install dependencies: `pip install -r requirements.txt`
- Start flask app: `python app.py`

## Update dependencies in requirements.txt (for devs)
- Go into venv
- Update current dependencies using `pip freeze > requirements.txt`

## Deprecated Gemini API update
1. In `app.py`, add `from google.api_core import exceptions as google_api_exceptions` alongside the existing imports so Gemini-specific errors can be caught explicitly.
2. Right after loading the environment variables, define `GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-1.5-flash")` to replace the hard-coded `gemini-1.0-pro` default.
3. Fully update `transform_phrase_gemini` in `app.py` to:
   - Abort early with a helpful message if `GEMINI_API_KEY` is missing.
   - Configure the Gemini client, instantiate `genai.GenerativeModel` with `model_name=GEMINI_MODEL_NAME`, and keep the existing temperature/top_p/top_k/max_output_tokens configuration.
   - Use `model.generate_content(prompt + phrase)` instead of the deprecated chat session flow.
   - Catch `google_api_exceptions.InvalidArgument` to return guidance about an invalid model name, and catch any other exception to surface a generic retry message.
   - Trim the returned text and provide a fallback message when no text is returned.
