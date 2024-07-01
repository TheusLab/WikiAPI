from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import wikipediaapi

app = Flask(__name__)
CORS(app)  # Adicionando suporte CORS

# Configurar a API do Wikipedia
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
wiki_wiki = wikipediaapi.Wikipedia(
    language='pt',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent=USER_AGENT
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def get_wiki_summary():
    topic = request.args.get('topic')
    if not topic:
        return jsonify({'error': 'No topic provided'}), 400
    
    page = wiki_wiki.page(topic)
    if page.exists():
        image_url = get_google_images(topic)
        return jsonify({'title': page.title, 'summary': page.summary, 'image_url': image_url})
    else:
        return jsonify({'error': 'Topic not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
