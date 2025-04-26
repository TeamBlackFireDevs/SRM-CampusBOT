from flask import Flask, render_template, request, jsonify
import sqlite3
from openai import OpenAI
from datetime import datetime
import os
from dotenv import load_dotenv
import markdown


# Load the .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
api_key = os.getenv("OPENROUTER_API_KEY")  # API key for OpenRouter

# Print API key status (safely)
print("Loaded API Key:", api_key[:8] + "..." if api_key else "None")

# Initialize OpenRouter-compatible client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:5000",  # Or your actual domain
        "X-Title": "srm-campus-chatbot"
    }
)

# Initialize Flask
app = Flask(__name__)

# Initialize SQLite database (not strictly necessary for SRM chatbot, but retained in case of future extensions)
def init_db():
    con = sqlite3.connect("srm_queries.db")
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY,
            question TEXT,
            response TEXT,
            timestamp TEXT
        )
    ''')
    con.commit()
    con.close()

# Home route - show the frontend
@app.route('/')
def home():
    print("Rendering index.html")
    return render_template('index.html')

# Chat route - talk to Mistral via OpenRouter
from flask import Flask, render_template, request, jsonify
import sqlite3
from openai import OpenAI
from datetime import datetime
import os
from dotenv import load_dotenv
import markdown


# Load the .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))
api_key = os.getenv("OPENROUTER_API_KEY")  # API key for OpenRouter

# Print API key status (safely)
print("Loaded API Key:", api_key[:8] + "..." if api_key else "None")

# Initialize OpenRouter-compatible client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:5000",  # Or your actual domain
        "X-Title": "srm-campus-chatbot"
    }
)

# Initialize Flask
app = Flask(__name__)

# Initialize SQLite database (not strictly necessary for SRM chatbot, but retained in case of future extensions)
def init_db():
    con = sqlite3.connect("srm_queries.db")
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY,
            question TEXT,
            response TEXT,
            timestamp TEXT
        )
    ''')
    con.commit()
    con.close()

# Home route - show the frontend
@app.route('/')
def home():
    print("Rendering index.html")
    return render_template('index.html')

# Chat route - talk to Mistral via OpenRouter
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    try:
        chat_response = client.chat.completions.create(
            model="mistralai/mistral-small-3.1-24b-instruct:free",  # Use a valid Mistral model available on OpenRouter
            messages=[
                {"role": "system", "content": "You are a helpful and informative assistant for SRM Institute of Science and Technology. Provide accurate information about SRM courses, fee structures, admissions, campus life, and more."},
                {"role": "user", "content": user_input}
            ]
        )
        markdown_reply = chat_response.choices[0].message.content
        html_reply = markdown.markdown(markdown_reply)

        # Optional: Save query to database
        con = sqlite3.connect("srm_queries.db")
        cur = con.cursor()
        cur.execute("INSERT INTO queries (question, response, timestamp) VALUES (?, ?, ?)",
                    (user_input, markdown_reply, datetime.now().isoformat()))
        con.commit()
        con.close()

        return jsonify({"response": html_reply})
    except Exception as e:
        print("OpenRouter Error:", e)
        return jsonify({"response": "Sorry, something went wrong.", "error": str(e)})


# Run the app
if __name__ == '__main__':
    init_db()
    print("Starting Flask server...")
    app.run(debug=True)
