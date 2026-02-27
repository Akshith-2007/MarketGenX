import os
import re
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)

groq_api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=groq_api_key) if groq_api_key else None

image_api_key = os.environ.get("IMAGE_API_KEY")

def generate_poster_image(prompt):
    """Generate poster image using OpenAI DALL-E API"""
    if not image_api_key:
        print("[poster] IMAGE_API_KEY not set")
        return None, "Error: IMAGE_API_KEY is not set"
    
    print(f"[poster] using key prefix: {image_api_key[:4]}...{image_api_key[-4:]}")
    try:
        headers = {
            "Authorization": f"Bearer {image_api_key}",
            "Content-Type": "application/json"
        }
        
        # use new image generation model per provided CURL example
        data = {
            "model": "gpt-image-1.5",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024"
        }
        
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=data,
            timeout=60
        )
        print(f"[poster] API response code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            image_url = result['data'][0]['url']
            return image_url, None
        else:
            err_text = response.text
            print(f"[poster] error body: {err_text}")
            # include key prefix in error for client debugging
            prefix = (image_api_key[:4] + '...' + image_api_key[-4:]) if image_api_key else 'none'
            return None, f"Error: {response.status_code} - {err_text} (key={prefix})"
    except Exception as e:
        print(f"[poster] exception: {e}")
        return None, f"An error occurred: {str(e)}"

def generate_with_groq(prompt):
    if not client:
        return "Error: GROQ_API_KEY is not set in the environment variables. Please add it to your .env file."
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are MarketAI, an expert marketing assistant. Provide professional, concise, and highly effective marketing content."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred while communicating with Groq: {str(e)}"

def format_campaign_output(text):
    if not text:
        return text
    
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            formatted_lines.append('<br>')
            continue
        
        if re.match(r'^#{1,6}\s', stripped):
            continue
        
        if re.match(r'^[A-Z][A-Za-z\s]+:$', stripped) or re.match(r'^[A-Z][A-Za-z\s]+\s*$', stripped) and len(stripped) < 50 and stripped.isupper() == False and stripped[0].isupper():
            if ':' in stripped or ('Team Member' in stripped):
                formatted_lines.append(f'<strong style="background: linear-gradient(120deg, #ff6b6b, #ee5a6f); color: white; padding: 8px 12px; border-radius: 4px; display: inline-block; margin: 5px 0;">{stripped}</strong>')
            else:
                formatted_lines.append(f'<h4 style="color: #ff6b6b; margin-top: 15px; margin-bottom: 10px; font-weight: bold; border-left: 4px solid #ff6b6b; padding-left: 10px;">{stripped}</h4>')
        else:
            formatted_lines.append(line)

    return '<br>'.join(formatted_lines)

def format_campaign_filter(text):
    return format_campaign_output(text)

app.jinja_env.filters['format_campaign'] = format_campaign_filter

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/campaign', methods=['GET', 'POST'])
def campaign():
    result = None
    if request.method == 'POST':
        product = request.form.get('product')
        audience = request.form.get('audience')
        goal = request.form.get('goal')
        team_members = int(request.form.get('team_members', 1))
        
        prompt = f"Create a comprehensive marketing campaign for a product/service: '{product}'. The target audience is '{audience}' and the primary goal is '{goal}'. Include suggested channels, key messaging, and 3 actionable steps. Additionally, assign specific tasks to {team_members} team members. For each team member (Team Member 1, Team Member 2, etc.), clearly specify their role and responsibilities in a structured format."
        result = generate_with_groq(prompt)
        
    return render_template('campaign.html', result=result)

@app.route('/generate-poster', methods=['POST'])
def generate_poster():
    campaign_content = request.json.get('campaign_content', '')
    
    if not campaign_content:
        return jsonify({'error': 'No campaign content provided'}), 400
    
    prompt = f"Based on this marketing campaign, create a compelling poster concept description with: 1) Main headline (max 10 words), 2) Supporting tagline (max 15 words), 3) Visual design suggestions, 4) Key visual elements to include, 5) Color scheme recommendations. Campaign details:\n\n{campaign_content}"
    
    poster_content = generate_with_groq(prompt)
    return jsonify({'poster': poster_content})

@app.route('/pitch', methods=['GET', 'POST'])
def pitch():
    result = None
    if request.method == 'POST':
        product = request.form.get('product')
        customer_profile = request.form.get('customer_profile')
        tone = request.form.get('tone', 'professional')
        
        prompt = f"Write a personalized sales pitch for '{product}'. The customer profile is '{customer_profile}' and the tone should be '{tone}'. Make it persuasive, addressing potential pain points and highlighting the value."
        result = generate_with_groq(prompt)
        
    return render_template('pitch.html', result=result)

@app.route('/poster', methods=['GET', 'POST'])
def poster():
    result = None
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        audience = request.form.get('audience')
        goal = request.form.get('goal')
        key_message = request.form.get('key_message')
        tone = request.form.get('tone', 'Professional')
        style = request.form.get('style', 'Modern Minimalist')
        color_preference = request.form.get('color_preference')
        additional_elements = request.form.get('additional_elements', '')
        
        prompt = (
            f"Create a detailed AI image prompt for generating a marketing poster.\n\n"
            f"Product: {product_name}\n"
            f"Target Audience: {audience}\n"
            f"Marketing Goal: {goal}\n"
            f"Key Message: {key_message}\n"
            f"Tone: {tone}\n"
            f"Visual Style: {style}\n"
            f"Color Scheme: {color_preference}\n"
            f"Additional Elements: {additional_elements if additional_elements else 'None'}\n\n"
            f"Generate a comprehensive prompt that includes:\n"
            f"- Detailed visual description\n"
            f"- Layout and composition\n"
            f"- Typography details\n"
            f"- Color specifications\n"
            f"- Imagery and elements\n"
            f"- Call-to-action placement\n"
            f"- Any special effects or styling\n\n"
            f"The prompt should be ready to use with DALL-E, Midjourney, Stable Diffusion, or similar AI image generators."
        )
        result = generate_with_groq(prompt)
        
    return render_template('poster.html', result=result)

@app.route('/lead-scorer', methods=['GET', 'POST'])
def lead_scorer():
    result = None
    if request.method == 'POST':
        name = request.form.get('name', '')
        demographic = request.form.get('demographic', '')
        behavior = request.form.get('behavior', '')
        financial = request.form.get('financial', '')
        engagement = request.form.get('engagement', '')
        need_fit = request.form.get('need_fit', '')

        prompt = f"""
You are a marketing analyst. Given the following lead details, provide:
1) A numeric lead score from 0-100.
2) A short rationale (2-4 sentences).
3) A recommended priority label (High / Medium / Low) and a 1-sentence suggested next action.

Lead details:
Name: {name}
Demographic: {demographic}
Behavior: {behavior}
Financial: {financial}
Engagement: {engagement}
Need / Problem Fit: {need_fit}

Respond concisely, with the score first on its own line, then the rationale and recommendation.
"""

        try:
            resp = generate_with_groq(prompt)
            result = resp
        except Exception as e:
            result = f"Error generating score: {e}"

    return render_template('lead_scorer.html', result=result)


@app.route('/competitor', methods=['GET', 'POST'])
def competitor():
    analysis = None
    if request.method == 'POST':
        product = request.form.get('product', '')
        competitors = request.form.get('competitors', '')
        market = request.form.get('market', '')
        features = request.form.get('features', '')

        prompt = f"""
You are an experienced product strategist. Provide a concise competitor analysis for the product below.
- Summarize the product positioning in one sentence.
- Compare it to the listed competitors across features, strengths, weaknesses, and target customers.
- Provide 3 tactical recommendations to differentiate and win in the {market} market.

Product: {product}
Competitors: {competitors}
Key features: {features}

Format with short headings and bullet points.
"""

        try:
            analysis = generate_with_groq(prompt)
        except Exception as e:
            analysis = f"Error generating analysis: {e}"

    return render_template('competitor.html', analysis=analysis)


@app.route('/faq', methods=['POST'])
def faq():
    data = request.get_json() or {}
    question = data.get('question', '')
    if not question:
        return jsonify({'answer': 'Please ask a question.'})
    prompt = f"You are MarketAI FAQ assistant. Provide clear concise answers to user questions about this marketing tool. FAQ question: {question}."
    answer = generate_with_groq(prompt)
    return jsonify({'answer': answer})

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.json
        user_message = data.get("message")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        prompt = f"""You are an expert marketing consultant for MarketAI Suite. 
        The user is asking: {user_message}
        
        Provide a concise, helpful response (2-3 sentences max) that:
        - Directly answers their question
        - Provides actionable advice
        - Relates to marketing campaigns, audience targeting, or campaign strategy
        
        Keep your response friendly and professional."""
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile"
        )
        
        response = chat_completion.choices[0].message.content
        
        return jsonify({"response": response})
    
    except Exception as e:
        print(f"Error in chatbot: {str(e)}")
        return jsonify({"error": f"Chatbot error: {str(e)}"}), 500

@app.route('/generate-poster-image', methods=['POST'])
def generate_poster_image_api():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        image_url, error = generate_poster_image(prompt)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'image_url': image_url, 'prompt': prompt})
    
    except Exception as e:
        print(f"Error generating poster image: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500

from io import BytesIO

if __name__ == '__main__':
    app.run(debug=True)
