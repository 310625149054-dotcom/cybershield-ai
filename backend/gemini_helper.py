import os
from dotenv import load_dotenv

load_dotenv()

# Provide a unified generate function that works with either the
# new `google-genai` package (`from google import genai`) or the
# older `google-generativeai` package (`import google.generativeai as genai`).

_GENMI_API_KEY = os.getenv("GEMINI_API_KEY")
_GENMI_MODEL = os.getenv("GEMINI_MODEL")

try:
    # New package: google-genai
    from google import genai

    _client = genai.Client(api_key=_GENMI_API_KEY)

    def _generate(prompt: str, model_name: str | None = None):
        model_name = model_name or _GENMI_MODEL or "gemini-2.0-flash"
        response = _client.models.generate_content(model=model_name, contents=prompt)
        return getattr(response, "text", None) or response.get("text") or str(response)

except Exception:
    # Fallback to older package name
    import google.generativeai as genai

    genai.configure(api_key=_GENMI_API_KEY)
    _model_name = _GENMI_MODEL or "gemini-1.5-flash"
    _model = genai.GenerativeModel(_model_name)

    def _generate(prompt: str, model_name: str | None = None):
        return _model.generate_content(prompt).text


def explain_url(url: str, result: str):
    prompt = f"""
    URL: {url}

    Detection Result: {result}

    Explain why this URL is safe or suspicious.
    Give a short cybersecurity recommendation.
    """

    return _generate(prompt)