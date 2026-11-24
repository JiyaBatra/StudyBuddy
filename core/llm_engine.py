import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

DEFAULT_GEMINI_MODEL = "gemini-3.5-flash-lite"


class GeminiAPIError(RuntimeError):
    pass


def configured_provider():
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    if provider != "gemini":
        return "demo"
    return "gemini" if os.getenv("GEMINI_API_KEY", "").strip() else "demo"


def generate(prompt, system_prompt="You are a patient personal tutor."):
    provider = configured_provider()
    if provider == "gemini":
        model = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip()
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        try:
            response = requests.post(
                url,
                headers={"x-goog-api-key": api_key},
                json={
                    "system_instruction": {"parts": [{"text": system_prompt}]},
                    "contents": [{"parts": [{"text": prompt}]}],
                },
                timeout=30,
            )
        except requests.RequestException as exc:
            raise GeminiAPIError("Could not connect to Gemini. Check your network and try again.") from exc

        if not response.ok:
            if response.status_code == 404:
                message = f"Gemini model '{model}' is unavailable. Check GEMINI_MODEL."
            elif response.status_code in {401, 403}:
                message = "Gemini rejected the API key or API access for this project."
            elif response.status_code == 429:
                message = "Gemini rate limit or quota reached. Try again later."
            else:
                message = f"Gemini request failed with HTTP {response.status_code}."
            raise GeminiAPIError(message)

        try:
            data = response.json()
        except ValueError as exc:
            raise GeminiAPIError("Gemini returned an unreadable response. Try again.") from exc

        candidates = data.get("candidates", [])
        if not candidates:
            raise GeminiAPIError("Gemini returned no answer. Try rephrasing the request.")
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(part.get("text", "") for part in parts if isinstance(part, dict))
        if not text:
            raise GeminiAPIError("Gemini returned no text. Try again.")
        return text
    return None


def generate_json(prompt, system_prompt="Return only valid JSON."):
    text = generate(prompt, system_prompt)
    if text is None:
        return None
    try:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end <= start:
            raise GeminiAPIError("Gemini did not return valid JSON. Please retry.")
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError as exc:
        raise GeminiAPIError("Gemini did not return valid JSON. Please retry.") from exc
