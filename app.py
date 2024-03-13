from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

# AI APIs
from openai import OpenAI
import google.generativeai as genai

app = Flask(__name__)
load_dotenv()

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
    
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=gemini_api_key)
    
    # Set up the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)


    # model = genai.GenerativeModel("gemini-pro")

    chat = model.start_chat(history=[])
    context = "In this chat, you will act as a phrase transformer, where you transform everyday phrases into phrases that are appropriate for a corporate setting. The tone of your transformed phrase should be cordial and pleasant, and exercise empathy for the external party. An example transformation to the phrase: 'Stay in your lane' would be 'To foster a harmonious and collaborative work environment, let's respectfully adhere to our defined roles and responsibilities.'  Please transform: "
    response = chat.send_message(context + phrase)
    
    return response.text
    # return "Wee you have transformed me to something corporate like using Google Gemini!"
    

if __name__ == '__main__':
    app.run(debug=True)