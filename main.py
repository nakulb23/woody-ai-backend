from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# 🔑 Replace this with your real Hugging Face token
HUGGINGFACE_TOKEN = "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"
MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}",
    "Content-Type": "application/json"
}

class Query(BaseModel):
    prompt: str

@app.post("/ask")
def ask_ai(query: Query):
    data = { "inputs": query.prompt }

    try:
        response = requests.post(MODEL_URL, headers=headers, json=data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e)
        print("Response text:", response.text)
        return {"error": "Hugging Face API returned an error."}
    except Exception as e:
        print("Request failed:", e)
        return {"error": "Failed to contact Hugging Face API."}

    try:
        result = response.json()
        print("Model output:", result)
        if isinstance(result, list) and "generated_text" in result[0]:
            return {"response": result[0]["generated_text"]}
        else:
            return {"error": "Unexpected response format from Hugging Face."}
    except Exception as e:
        print("JSON decoding error:", e)
        print("Raw response text:", response.text)
        return {"error": "Failed to parse response from Hugging Face."}
