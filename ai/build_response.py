from ollama import Client
from django.conf import settings


client = Client(
    host=settings.OLLAMA_HOST
)


def generate_response(prompt):
    response = client.chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.message.content.strip()