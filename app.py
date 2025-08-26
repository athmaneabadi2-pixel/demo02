import os
from flask import Flask, request, jsonify, Response
import html
from dotenv import load_dotenv
from config import DISPLAY_NAME, INSTANCE_LABEL, TIMEZONE, FEATURES, PROFILE_PATH
from core.llm import generate_reply
from core.memory import Memory
from infra.monitoring import health_payload

load_dotenv()

app = Flask(__name__)
memory = Memory(profile_path=PROFILE_PATH)

@app.get("/health")
def health():
    return jsonify(health_payload(instance_label=INSTANCE_LABEL)), 200

@app.post("/internal/send")
def internal_send():
    # Sécurité simple par jeton
    if request.headers.get("X-Token") != os.getenv("INTERNAL_TOKEN"):
        return jsonify({"error": "forbidden"}), 403

    data = request.json or {}
    text = data.get("text", "Bonjour")
    profile = memory.get_profile()
    reply = generate_reply(text, profile)

    # Supporte ?format=text pour les checks simples
    if (request.args.get("format") or "").lower() == "text":
        return Response(reply, mimetype="text/plain; charset=utf-8"), 200

    return jsonify({"ok": True, "request_text": text, "reply": reply}), 200

@app.post("/whatsapp/webhook")
def whatsapp_webhook():
    incoming = request.form or request.json or {}
    text = (incoming.get("Body") or incoming.get("text") or "").strip() or "Salut"
    profile = memory.get_profile()
    reply = generate_reply(text, profile)
    twiml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{html.escape(reply)}</Message></Response>'
    return Response(twiml, mimetype="application/xml")
