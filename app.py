PROXY_URL = "https://fal-proxy-beast.onrender.com/api/fal/proxy"

headers = {
    "x-fal-target-url": f"{FAL_BASE_URL}/{selected_model}",
    "Content-Type": "application/json"
}

response = requests.post(PROXY_URL, headers=headers, json=payload)
