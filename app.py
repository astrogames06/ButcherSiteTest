from flask import Flask, render_template, request, jsonify
import os
from openai import OpenAI
from flask_cors import CORS

app = Flask(__name__,
    static_url_path='',
)
CORS(app)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AI_INFO = """
You are a helpful assistant for Papa Joe's Chicken restaurant website. 
Here is information you should know:

- Papa Joe's Chicken is a small, friendly restaurant serving hot, crispy chicken.
- The restaurant is cozy, staff are kind, and people come for quick, tasty meals.
- Location: 33 Huffin Puffin Rd, Rosebay.
- Menu:
    - Soda: $1
    - Chips: $2
    - Whole Roast Chicken: $5
- Hours:
    - Monday to Friday: 8AM - 8PM
    - Saturday to Sunday: 10AM - 5PM
- Contact phone: +61404907277
- You are polite and helpful. Only answer questions about the restaurant and related topics.

Always try to answer based on this information.
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gpt", methods=["POST"])
def api():
    data = request.json
    text = data.get("text", "")
    model = data.get("model", "gpt-4.1-mini")

    print(model)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": AI_INFO},
            {"role": "user", "content": text}
        ]
    )
    
    output = response.choices[0].message.content
    return jsonify({"output": output})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)