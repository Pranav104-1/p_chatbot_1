from flask import Flask, request, jsonify, render_template
import cohere
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__,static_folder='static', static_url_path='/static')
co = cohere.ClientV2(os.getenv('API_KEY'))



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' key"}), 400

        user_prompt = data['prompt']
        response = co.chat(
            model="command-a-03-2025",
            messages=[{"role": "system", "content": user_prompt}, {"role": "user", "content": "Hello!"}]
        )

        print("Cohere API Full Response:", response)

        if hasattr(response, "message") and hasattr(response.message, "content"):
            assistant_message = response.message.content[0].text
            return jsonify({"response": assistant_message})
        else:
            return jsonify({"error": "Unexpected response format"}), 500

    except Exception as e:
        print(f"Error: {e}")  
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
