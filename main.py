@app.post("/ask")
def ask_ai(query: Query):
    data = { "inputs": query.prompt }
    response = requests.post(MODEL_URL, headers=headers, json=data)

    try:
        response.raise_for_status()  # Raise error for bad HTTP codes
    except requests.exceptions.HTTPError as e:
        print("Hugging Face returned an error:")
        print(response.status_code)
        print(response.text)
        return {"error": "Hugging Face API error"}

    try:
        result = response.json()
        print("Hugging Face response:", result)
        if isinstance(result, list) and "generated_text" in result[0]:
            return {"response": result[0]["generated_text"]}
        else:
            return {"error": "Unexpected response format"}
    except Exception as e:
        print("JSON decode error:", e)
        print("Raw response:", response.text)
        return {"error": "Could not parse JSON from Hugging Face"}
