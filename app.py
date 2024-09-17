from flask import Flask, render_template, request
from textblob import TextBlob
import google.generativeai as palm
import os
import openai

# Configure the API keys
palm_api_key = "YOUR_PALM_API_KEY"
palm.configure(api_key=palm_api_key)

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/ai_agent", methods=["GET", "POST"])
def ai_agent():
    return render_template("ai_agent.html")

@app.route("/ai_agent_reply", methods=["POST"])
def ai_agent_reply():
    q = request.form.get("q")
    try:
        # OpenAI GPT-3.5 API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": q}],
        )
        r = response.choices[0].message['content']
    except Exception as e:
        r = f"Error: {str(e)}"
    
    return render_template("ai_agent_reply.html", r=r)

@app.route("/singapore_joke", methods=["POST"])
def singapore_joke():
    joke = "The only thing faster than Singapore's MRT during peak hours is the way we 'chope' seats with a tissue packet."
    return render_template("joke.html", joke=joke)

@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    return render_template("index.html")

@app.route("/textblob", methods=["GET"])
def textblob():
    return render_template("textblob.html")

@app.route("/textblob_analysis", methods=["POST"])
def textblob_analysis():
    text = request.form.get("text")
    
    if text:
        blob = TextBlob(text)
        sentiment = blob.sentiment
        return render_template("textblob_result.html", sentiment=sentiment)
    else:
        return "Please provide text for analysis."

if __name__ == "__main__":
    app.run(debug=True)
