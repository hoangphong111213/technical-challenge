from flask import Flask, request, jsonify
import requests
import time
import csv
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = {
    "gemini": "google/gemini-2.5-flash",
    "mistral": "mistralai/mistral-7b-instruct:free"
}

os.makedirs('logs', exist_ok=True)

def count_tokens(text):
    """Simple token counting (approximate)"""
    return len(text.split())

def log_request(model, prompt, response, latency, prompt_tokens, response_tokens):
    """Log request details to CSV file"""
    log_file = 'logs/requests.csv'
    if not os.path.exists(log_file):
        with open(log_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp', 'model', 'prompt', 'response', 
                'latency_ms', 'prompt_tokens', 'response_tokens'
            ])
    
    with open(log_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            model,
            prompt[:300] + "..." if len(prompt) > 300 else prompt,
            response[:300] + "..." if len(response) > 300 else response,
            latency,
            prompt_tokens,
            response_tokens
        ])

def call_openrouter_api(model_name, prompt):
    """Call OpenRouter API with the specified model"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODELS[model_name],
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    start_time = time.time()
    
    try:
        response = requests.post(OPENROUTER_BASE_URL, headers=headers, json=data)
        response.raise_for_status()
        
        end_time = time.time()
        latency = int((end_time - start_time) * 1000)  # Convert to milliseconds
        
        result = response.json()
        
        if 'choices' in result and len(result['choices']) > 0:
            response_text = result['choices'][0]['message']['content']
            
            prompt_tokens = count_tokens(prompt)
            response_tokens = count_tokens(response_text)
            
            log_request(model_name, prompt, response_text, latency, prompt_tokens, response_tokens)
            
            return {
                "success": True,
                "response": response_text,
                "latency_ms": latency,
                "prompt_tokens": prompt_tokens,
                "response_tokens": response_tokens,
                "model": model_name
            }
        else:
            return {"success": False, "error": "No response from model"}
            
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"API request failed: {str(e)}"}

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        "message": "LLM Service API",
        "endpoints": {
            "/chat": "POST - Send a prompt to an LLM",
            "/models": "GET - List available models",
            "/logs": "GET - View request logs"
        },
        "example": {
            "url": "/chat",
            "method": "POST",
            "body": {
                "prompt": "Hello, how are you?",
                "model": "llama"
            }
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        prompt = data.get('prompt')
        model = data.get('model', 'llama')  # Default to llama
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        if model not in MODELS:
            return jsonify({
                "error": f"Invalid model. Choose from: {list(MODELS.keys())}"
            }), 400
        
        result = call_openrouter_api(model, prompt)
        
        if result["success"]:
            return jsonify({
                "prompt": prompt,
                "response": result["response"],
                "model": result["model"],
                "latency_ms": result["latency_ms"],
                "tokens": {
                    "prompt": result["prompt_tokens"],
                    "response": result["response_tokens"]
                }
            })
        else:
            return jsonify({"error": result["error"]}), 500
            
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/models', methods=['GET'])
def get_models():
    """Get available models"""
    return jsonify({
        "available_models": list(MODELS.keys()),
        "model_details": MODELS
    })

@app.route('/logs', methods=['GET'])
def get_logs():
    """Get recent logs"""
    log_file = 'logs/requests.csv'
    
    if not os.path.exists(log_file):
        return jsonify({"logs": [], "message": "No logs found"})
    
    logs = []
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            logs = list(reader)
        
        return jsonify({"logs": logs[-10:], "total_requests": len(logs)})
    except Exception as e:
        return jsonify({"error": f"Failed to read logs: {str(e)}"}), 500

if __name__ == '__main__':
    print("Starting LLM Service...")
    print("Available models:", list(MODELS.keys()))
    print("API Key configured:", "Yes" if OPENROUTER_API_KEY else "No")
    app.run(debug=True, host='0.0.0.0', port=5001)