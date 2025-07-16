# technical-challenge

## Quick Start
### Prerequisites
* Python 3.10
* OpenRouter API key

### Installation
1. Clone the repository
````bash
git clone <your-repo-url>
cd llm-service
````

2. Install dependencies
````bash
pip install -r requirements.txt
````

3. Set up environment variables: Create a .env file in the root directory:
````env
OPENROUTER_API_KEY=your_api_key_here
````

4. Run the service
````bash
python app.py
````

5. Testing
````bash
python test.py
````

### Sample test output
````bash
Testing LLM Service...
==================================================

Testing model: gemini
------------------------------

Test 1: What is the capital of France?
✅ Success!
Response: The capital of France is **Paris**.
Latency: 3062ms
Tokens: 6 -> 6
````

### Sample log file
```csv
timestamp,model,prompt,response,latency_ms,prompt_tokens,response_tokens
2025-07-16T23:54:07.052852,gemini,What is the capital of France?,The capital of France is **Paris**.,3062,6,6
2025-07-16T23:54:13.541708,gemini,"Explain quantum computing in simple terms, less than 200 characters.",Quantum computers use tiny particles' weird rules (superposition & entanglement) to solve complex problems faster than regular computers.,5473,10,18
2025-07-16T23:54:17.448802,gemini,"Write a short poem, less than 200 characters, about coding.","Logic's loom, Ideas bloom. Code's a song, Making dreams strong.",2894,10,10
2025-07-16T23:54:21.202364,mistral,What is the capital of France?," The capital of France is Paris. It is located in the north-central part of the country. Paris is known for its iconic landmarks such as the Eiffel Tower, Louvre Museum, Notre-Dame Cathedral...",2735,6,48

