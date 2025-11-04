from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

# AI APIs
from openai import OpenAI
from google import genai
from google.api_core import exceptions as google_api_exceptions

app = Flask(__name__)
load_dotenv()

GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.5-flash")

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transform', methods=['POST'])
def transform():
    input_phrase = request.form['input_phrase']
    
    # Call the OpenAI API to transform the phrase
    # transformed_phrase = transform_phrase_OpenAI(input_phrase)

    # Call Gemini
    transformed_phrase = transform_phrase_gemini(input_phrase)
    
    return render_template('result.html', input_phrase=input_phrase, transformed_phrase=transformed_phrase)

# Other functions


# Calling openAI in this function
# OpenAI api calls heavily references https://www.youtube.com/watch?v=fiugJ8FfYOk
def transform_phrase_OpenAI(phrase):
    # Role:user is basically us, the user
    # Role:assistant is ChatGPT
    # Role:system is giving ChatGPT its context (ie. You are a phrase transformer, where you transform everyday phrases into phrases that are appropriate for a corporate setting)
    
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)

    response = client.chat.completions.create(
        messages=[
            {
                "role":"system",
                "content":"You are a phrase transformer, where you transform everyday phrases into phrases that are appropriate for a corporate setting"
            },
            {
                "role":"user",
                "content": phrase
            }
        ],
        model="gpt-3.5-turbo-0125" #Most cost effective that allows me to do what I need
    )

    return response.choices[0].message.content
    # return "Wee you have transformed me to something corporate like using OpenAI!"


# Same functionality, but uses Gemini API instead, reference: https://www.youtube.com/watch?v=nftMAclfeMM
def transform_phrase_gemini(phrase):
    
    gemini_api_key = (
        # os.environ.get("GEMINI_API_KEY")
        os.environ.get("GEMINI_API_KEY_GAISTUDIO")
        # or os.environ.get("GEMINI_API_KEY_GCLOUD")
    )
    
    if not gemini_api_key:
        print("ERROR: No Gemini API key is configured")
        return "Unable to process your request. Please contact support."
    
    try:
        client = genai.Client(api_key=gemini_api_key)

        prompt = ("In this chat, you will act as a phrase transformer, where you transform everyday phrases into phrases that are appropriate for a corporate setting. The tone of your transformed phrase should be cordial and pleasant, and exercise empathy for the external party. An example transformation to the phrase: 'Stay in your lane' would be 'To foster a harmonious and collaborative work environment, let's respectfully adhere to our defined roles and responsibilities.'  Please transform: ")

        
        response = client.models.generate_content(
            model=GEMINI_MODEL_NAME,
            contents=prompt + phrase,
        )
        
        result_text = response.text.strip() if getattr(response, "text", None) else ""
        
        if not result_text:
            print("WARNING: Empty response from Gemini API")
            return "No response generated. Please try again with a different phrase."
        
        return result_text
        
    except google_api_exceptions.GoogleAPIError as e:
        print(f"ERROR: Gemini API returned an error - {str(e)}")
        if isinstance(e, google_api_exceptions.NotFound):
            return "The AI model is not available. Please try again later."
        return "Unable to transform your phrase at this time. Please try again later."
    except Exception as e:
        print(f"ERROR: Gemini client failure - {str(e)}")
        return "Unable to transform your phrase at this time. Please try again later."
    

if __name__ == '__main__':
    app.run(debug=True)
