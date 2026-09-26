from google.genai import Client
from django.conf import settings

key=settings.GEMINI_API_KEY

client = Client(api_key=key)

def generate_response(prompt):
    response = client.models.generate_content(
    model='gemini-flash-2.5',
    contents=prompt)
    return response.text.strip()