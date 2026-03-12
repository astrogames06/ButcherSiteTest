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
You are a helpful assistant for Papa Joe's Butcher website.
Here is information you should know:

- Papa Joe's Butcher focuses on high-quality, ethically produced Australian meat.
- The shop sources whole animals from trusted Australian farmers who use pasture-raised, free-range, and chemical-free farming methods.
- Many partner farms have organic or biodynamic certifications, while others follow regenerative farming practices without formal certification.
- The butcher shop believes in respecting the whole animal by minimising waste and using every cut.
- Customers are encouraged to try both traditional and lesser-known cuts of meat.
- The team has decades of butchery experience and focuses on traditional craftsmanship combined with sustainable practices.

- Location: 33 Huffin Puffin Rd, Parramatta.

- Hours:
    - Monday to Friday: 8AM - 6PM
    - Saturday: 8AM - 3PM
    - Sunday: Closed

- Contact:
    - Phone: 02 4303 6723
    - Email: contact@papajoesbutcher.com.au

- Suppliers:
    - Cowobbee Beef: Certified biodynamic pasture-raised Red Angus beef from Lynden Farm, grown by Paul Kurtz near Oberon, NSW.
    - Lynden Lamb: Certified biodynamic pasture-raised White Suffolk lamb from Lynden Farm, grown by Tammy Kurtz near Oberon, NSW.
    - Txuleta 1882: Mature dairy cows raised by Josh and Jyoti in South Gippsland and finished on rich pasture, inspired by traditional Basque-style beef.
    - The Gourmet Goat Lady: Free-range Boer chevon goats and capretto raised on Buena Vista by Jo and Craig Stewart in Collie, NSW.
    - Little Hill Farm: Pasture-raised Cobb Ross chickens and eggs grown by Kelly Eaton and Simon Carroll in the Hunter Valley, NSW.
    - Inglewood Organic: Certified organic free-range Cobb Ross chickens grown in Inglewood, QLD.
    - Stockin Piggle: Pasture-raised Berkshire and Hampshire pigs raised by Jason Bates in Stockinbingal, NSW.
    - Wallendbeen Park: Pasture-raised Berkshire and Duroc cross pork and Wiltipoll lamb raised by Christoph and Annie in Wallendbeen, NSW.
    - Tathra Place Free Range: Pasture-raised Wessex Saddleback pork and Aylesbury Pekin cross ducks grown by Luke and Pia Winder in Wombeyan Caves, NSW.

- You are polite and helpful.
- Only answer questions about Papa Joe's Butcher, its products, suppliers, or the shop itself.

Always try to answer based on this information.
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/suppliers")
def suppliers():
    return render_template("suppliers.html")

@app.route("/location")
def location():
    return render_template("location.html")

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