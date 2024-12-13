# app.py
from flask import Flask, request, jsonify
import json
from datetime import datetime
import os
from functools import wraps
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get API keys from GitHub environment variable
API_KEYS = os.environ.get('GMASS_API_KEYS', '').split(',')

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-apikey')
        
        if not api_key:
            logger.warning("No API key provided in request")
            return jsonify({"error": "No API key provided"}), 401
            
        if api_key not in API_KEYS:
            logger.warning(f"Invalid API key attempted: {api_key[:4]}...")
            return jsonify({"error": "Invalid API key"}), 401
            
        return f(*args, **kwargs)
    return decorated_function

def log_event(event_type, data):
    """Log event data"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{timestamp}] New {event_type.upper()} Event")
    logger.info(f"API Key: ...{request.headers.get('X-apikey')[-4:]}")
    logger.info(f"Data: {json.dumps(data)}")

@app.route('/')
def home():
    return jsonify({
        "status": "active",
        "message": "GMass Webhook Server is running",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/webhook/opens', methods=['POST'])
@require_api_key
def handle_opens():
    log_event('opens', request.json)
    return jsonify({"status": "success"}), 200

@app.route('/webhook/clicks', methods=['POST'])
@require_api_key
def handle_clicks():
    log_event('clicks', request.json)
    return jsonify({"status": "success"}), 200

@app.route('/webhook/replies', methods=['POST'])
@require_api_key
def handle_replies():
    log_event('replies', request.json)
    return jsonify({"status": "success"}), 200

@app.route('/webhook/bounces', methods=['POST'])
@require_api_key
def handle_bounces():
    log_event('bounces', request.json)
    return jsonify({"status": "success"}), 200

@app.route('/webhook/unsubscribes', methods=['POST'])
@require_api_key
def handle_unsubscribes():
    log_event('unsubscribes', request.json)
    return jsonify({"status": "success"}), 200

@app.route('/webhook/sends', methods=['POST'])
@require_api_key
def handle_sends():
    log_event('sends', request.json)
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    if not API_KEYS or API_KEYS[0] == '':
        logger.error("No API keys configured! Check GitHub environment variables.")
        exit(1)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)