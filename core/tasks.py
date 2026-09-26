from youtube_transcript_api import YouTubeTranscriptApi
from celery import shared_task
from .models import Summary
from django.shortcuts import get_object_or_404
from urllib.parse import urlparse, parse_qs
from ai.final_response import final_response

@shared_task
def TranscriptFetch(id):
    api = YouTubeTranscriptApi()
    obj=get_object_or_404(Summary.objects.select_related('user'), id=id)
    query = parse_qs(urlparse(obj.link).query)
    video_id = query.get("v", [None])[0]
    transcript = api.fetch(video_id)
    final=''
    for snippet in transcript:
        final=final+snippet.text
    response=final_response(transcript=final)
    obj.transcript=final
    obj.summary=response
    obj.save()
    return f"transcript and ai_response saved for id:{id}"

# @shared_task
# def airesponsegeneration(transcript, id):
#     response=final_response(transcript=transcript)
#     data=get_object_or_404(Summary, id=id)
#     data.summary=response
#     data.save()
#     return f"ai_response saved for id:{id}"