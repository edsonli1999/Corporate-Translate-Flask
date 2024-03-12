from flask import Flask, render_template, request
from dotenv import load_dotenv
import openai
import os

app = Flask(__name__)
load_dotenv()
# Chatgpt suggestion
# openai.api_key = os.getenv("OPENAI_API_KEY")
# Vercel suggestion, both seems to work
my_api_key = os.environ.get("OPENAI_API_KEY")
openai.api_key = my_api_key

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transform', methods=['POST'])
def transform():
    input_phrase = request.form['input_phrase']
    
    # Call the OpenAI API to transform the phrase
    transformed_phrase = transform_phrase(input_phrase)
    
    return render_template('result.html', input_phrase=input_phrase, transformed_phrase=transformed_phrase)

# Other functions

def transform_phrase(phrase):
    # Call the OpenAI API to transform the phrase
    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=f"Transform the following phrase into a corporate version: '{phrase}'",
    #     max_tokens=50
    # )
    
    # return response.choices[0].text.strip()

    return "Wee you have transformed me to something corporate like!"

if __name__ == '__main__':
    app.run(debug=True)