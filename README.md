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

# Getting Started

## Running a local server
- To go into VENV: `venv\Scripts\activate`. To escape venv: `deactivate`
- To run flask app: `python app.py`

## First time (if no venv folder exits)
- Create a new venv: `python -m venv venv`
- activate venv: `venv/scripts/acivate`
- Install dependencies: `pip install -r requirements.txt`
- Start flask app: `python app.py`

## Updating dependencies (for devs)
- Go into venv
- Update current dependencies using `pip freeze > requirements.txt`

# TODOs:

## Gemini Update:

Checklist to migrate the deprecated `google-generativeai` implementation to the supported `google-genai` client and Gemini 2.5 Flash.

### Environment configuration
- Continue loading environment variables with `python-dotenv`, then set `GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.5-flash")` so the default model upgrades from `gemini-1.5-flash`.
- Replace the single-line `gemini_api_key = os.environ.get("GEMINI_API_KEY")` with the following block so the GA Studio key is prioritised while keeping the legacy name as a commented reminder:
  ```python
  gemini_api_key = (
      # os.environ.get("GEMINI_API_KEY")
      os.environ.get("GEMINI_API_KEY_GAISTUDIO")
      # or os.environ.get("GEMINI_API_KEY_GCLOUD")
  )
  ```
- Leave the guard clause right after this assignment; update it to log `ERROR: No Gemini API key is configured` before returning `"Unable to process your request. Please contact support."`

### Python dependencies
- In `requirements.txt`, remove `google-generativeai` and `google-ai-generativelanguage`.
- Add the replacement dependency `google-genai==0.1.0`.
- Keep the existing `google-api-core`, `google-auth`, and gRPC packages so error handling continues to work.

### Implementation steps (`app.py`)
1. Change the import from `import google.generativeai as genai` to `from google import genai`. Keep the existing `google.api_core.exceptions` import.
2. Remove the global `genai.configure(...)` call; instead, instantiate the client inside `transform_phrase_gemini` with `client = genai.Client(api_key=gemini_api_key)`.
3. Preserve the descriptive prompt string (including the "Stay in your lane" example) and call the new client with:
   ```python
   response = client.models.generate_content(
       model=GEMINI_MODEL_NAME,
       contents=prompt + phrase,
   )
   ```
4. When extracting the result, use `response.text.strip()` and guard it with `getattr(response, "text", None)` so missing fields do not crash the app. If the text is empty, log `WARNING: Empty response from Gemini API` and return `"No response generated. Please try again with a different phrase."`

### Error handling conventions
- Wrap the Gemini call in `try/except google_api_exceptions.GoogleAPIError as e`.
- If `isinstance(e, google_api_exceptions.NotFound)`, return `"The AI model is not available. Please try again later."`
- For all other `GoogleAPIError` instances, log `ERROR: Gemini API returned an error - ...` and return `"Unable to transform your phrase at this time. Please try again later."`
- Add a broad `except Exception as e` handler that logs `ERROR: Gemini client failure - ...` and returns the same generic retry message.


## UI Update
Whilst waiting for a response from the model, there isn't a feedback on the UI, resulting in poor UX and possibility for people to send multiple requests.

### Fix options:
- (Easiest) Disable 'transform' button and change text to something like "Loading..."
- (More ideal UX) Load result page first but have skeleton pulsating loaders if response still hasn't come it yet
