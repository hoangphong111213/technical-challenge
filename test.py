import requests
import json
import time

BASE_URL = "http://localhost:5001"

def test_chat_endpoint():
    """Test the chat endpoint with both models"""
    
    test_prompts = [
        "What is the capital of France?",
        "Explain quantum computing in simple terms, less than 200 characters.",
        "Write a short poem, less than 200 characters, about coding."
    ]
    
    models = ["gemini", "mistral"]
    
    print("Testing LLM Service...")
    print("=" * 50)
    
    for model in models:
        print(f"\nTesting model: {model}")
        print("-" * 30)
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\nTest {i}: {prompt}")
            
            try:
                response = requests.post(f"{BASE_URL}/chat", json={
                    "prompt": prompt,
                    "model": model
                })
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Success!")
                    print(f"Response: {data['response'][:300]}...")
                    print(f"Latency: {data['latency_ms']}ms")
                    print(f"Tokens: {data['tokens']['prompt']} -> {data['tokens']['response']}")
                else:
                    print(f"❌ Error: {response.status_code}")
                    print(f"Response: {response.text}")
                
                # Small delay between requests
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Exception: {e}")

def test_other_endpoints():
    """Test other endpoints"""
    print("\n" + "=" * 50)
    print("Testing other endpoints...")
    
    # Test models endpoint
    try:
        response = requests.get(f"{BASE_URL}/models")
        if response.status_code == 200:
            print("✅ Models endpoint working")
            print(f"Available models: {response.json()['available_models']}")
        else:
            print(f"❌ Models endpoint error: {response.status_code}")
    except Exception as e:
        print(f"❌ Models endpoint exception: {e}")
    
    try:
        response = requests.get(f"{BASE_URL}/logs")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Logs endpoint working")
            print(f"Total requests logged: {data.get('total_requests', 0)}")
        else:
            print(f"❌ Logs endpoint error: {response.status_code}")
    except Exception as e:
        print(f"❌ Logs endpoint exception: {e}")

if __name__ == "__main__":
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("Service is running!")
            test_chat_endpoint()
            test_other_endpoints()
        else:
            print("Service not responding correctly")
    except Exception as e:
        print(f"Cannot connect to service: {e}")
        print("Make sure the service is running with: python app.py")