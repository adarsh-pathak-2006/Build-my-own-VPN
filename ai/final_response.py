from .build_response import generate_response
from .build_prompt import prompt

def final_response(transcript):
    p=prompt(transcript=transcript)
    response=generate_response(prompt=p)
    return response