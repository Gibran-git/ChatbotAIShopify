import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    global client
    print("Request received at /api/chat endpoint")
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are a knowledgeable customer service assistant for Gibb&Daan, a luxury flatware brand. 

    Product Information:
    - We specialize in high-end flatware including:
    * Cutlery sets
    * Serving bowls
    * Serving sets
    * Cake sets
    * And other luxury dining accessories
    - We offer custom laser engraving services for personalization
    - Customers can submit their own designs for engraving on any flatware piece
    - All our products are made with premium materials and exceptional craftsmanship

    Customization Services:
    - Custom laser engraving available on all flatware
    - Customers can provide their own design for engraving
    - Perfect for:
    * Wedding gifts
    * Corporate gifts
    * Special occasions
    * Personal customization
    * Family heirlooms

    Shipping Information:
    - Shipping costs are calculated at checkout
    - Prices vary based on location and order size
    - Secure packaging to protect luxury items

    Return Policy:
    - 30-day return window
    - Full refunds provided for returned items
    - Items must be in original condition with packaging

    Please provide elegant, professional responses that reflect our luxury brand image. Be helpful and informative about our products and customization options. If customers have specific questions about shipping costs, direct them to proceed to checkout for accurate calculations. For detailed customization requests, encourage them to contact our customer service team.

    Always maintain a tone that reflects our premium brand positioning."""},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=250,  
                temperature=0.7
            )

        bot_response = response.choices[0].message.content.strip()
        return jsonify({'response': bot_response})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return 'Welcome to the Chatbot API! Use the /api/chat endpoint to chat.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))