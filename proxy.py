from flask import Flask, request, Response
import requests
import os
import urlparse

app = Flask(__name__)

FAL_KEY = os.environ.get("FAL_KEY")
if not FAL_KEY:
    raise ValueError("FAL_KEY environment variable required")

ALLOWED_DOMAINS = ["fal.ai", "fal.run"]

@app.route("/api/fal/proxy", methods=["GET", "POST"])
def fal_proxy():
    target_url = request.headers.get("x-fal-target-url")
    if not target_url:
        return "Missing x-fal-target-url header", 400

    try:
        parsed = urlparse.urlparse(target_url)
        if not parsed.netloc.endswith(tuple(ALLOWED_DOMAINS)):
            return "Invalid domain", 412
    except:
        return "Invalid URL", 412

    if request.method not in ["GET", "POST"]:
        return "Method Not Allowed", 405

    if request.content_type != "application/json":
        return "Unsupported Media Type", 415

    headers = {
        "Authorization": f"Key {FAL_KEY}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            json=request.get_json() if request.data else None,
            stream=True,
            timeout=120
        )
        
        excluded_headers = ["content-encoding", "content-length"]
        response_headers = [(name, value) for name, value in resp.raw.headers.items() if name.lower() not in excluded_headers]
        
        return Response(resp.content, resp.status_code, response_headers)
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
