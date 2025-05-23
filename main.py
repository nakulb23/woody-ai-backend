from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

HUGGINGFACE_TOKEN = "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"  # <- Replace this with your token
MODEL_URL = "https://api-inference.huggingface.co/models/eidorb90/Woody.AI"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_TOKEN}"
}

class Query(BaseModel):
    prompt: str

@app.post("/ask")
def ask_ai(query: Query):
    data = {
        "inputs": query.prompt
    }
    response = requests.post(MODEL_URL, headers=headers, json=data)
    if response.status_code == 200:
        return {"response": response.json()[0]["generated_text"]}
    else:
        return {"error": response.json()}

