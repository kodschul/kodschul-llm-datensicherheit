import requests

response = requests.post(
    # 7869 11434
    "http://localhost:11434/api/generate",
    json={
        "model": "gemma:2b", 
          "prompt": "Nenne drei Vorteile von Solarenergie", 
          "stream": False})
data = response.json()["response"]


print(data)
