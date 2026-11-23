"""
Minimal REST backend for the Computer Networks course project.
Run the SAME file for Backend A (BACKEND_ID=A, PORT=3001) and
Backend B (BACKEND_ID=B, PORT=3002).

Usage:
    BACKEND_ID=A PORT=3001 python3 app.py
"""
import os
import socket
from flask import Flask, jsonify, make_response, request
from werkzeug.serving import make_server

app = Flask(__name__)
BACKEND_ID = os.environ.get("BACKEND_ID", "A")
PORT = int(os.environ.get("PORT", 3001))
CACHE_TAG = "cn-cache-v1"


@app.route("/")
def home():
    resp = make_response(
        jsonify(
            backend=BACKEND_ID,
            message=f"Backend {BACKEND_ID} is running",
            hostname=socket.gethostname(),
        )
    )
    resp.headers["X-Backend"] = BACKEND_ID
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.route("/api/status")
def status():
    resp = make_response(
        jsonify(
            backend=BACKEND_ID,
            status="ok",
            hostname=socket.gethostname(),
        )
    )
    resp.headers["X-Backend"] = BACKEND_ID
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.route("/api/cache")
def cache():
    if request.if_none_match.star_tag or request.if_none_match.contains_weak(CACHE_TAG):
        resp = make_response("", 304)
    else:
        resp = jsonify(
            message="CN cache example",
            cached_data="Fresh response from server",
        )
    resp.headers["X-Backend"] = BACKEND_ID
    resp.set_etag(CACHE_TAG)
    resp.headers["Cache-Control"] = "public, max-age=60"
    return resp


if __name__ == "__main__":
    # Pre-bind so startup does not need a reverse DNS lookup on the lab LAN.
    with socket.create_server(("0.0.0.0", PORT)) as listener:
        server = make_server("0.0.0.0", PORT, app, threaded=True, fd=listener.fileno())
    print(f"Backend {BACKEND_ID} listening on 0.0.0.0:{PORT}", flush=True)
    server.serve_forever()
