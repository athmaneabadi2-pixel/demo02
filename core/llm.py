def generate_reply(text: str, profile: dict) -> str:
    """
    Faux générateur de réponse (placeholder).
    Remplace plus tard par un appel OpenAI/LLM et un prompt adapté.
    """
    user_name = profile.get("user", {}).get("display_name", "ami")
    if not text.strip():
        return f"Salut {user_name} ! Dis-moi, comment te sens-tu aujourd'hui ?"
    lower = text.lower()
    if "météo" in lower:
        return "Voici la météo du jour ☁️ (démo)."
    if "sport" in lower:
        return "Derniers résultats NBA (démo)."
    return f"Merci {user_name} 🙏 Je suis là. Tu m'écris : “{text}”."
