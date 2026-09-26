from .build_response import generate_response
from .build_prompt import prompt
from django.shortcuts import get_object_or_404
from core.models import Summary

def final_response(transcript, id):
    p=prompt(transcript=transcript)
    response=generate_response(prompt=p)
    data=get_object_or_404(Summary, id=id)
    data.summary=response
    data.save()
    return response