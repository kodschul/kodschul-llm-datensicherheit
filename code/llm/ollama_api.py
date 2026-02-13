import requests

response = requests.post(
    # 7869 11434
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.2:1b",
        "prompt": "Nenne drei Vorteile von Solarenergie",
        "stream": False})
data = response.json()


print(data)
