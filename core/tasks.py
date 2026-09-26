from youtube_transcript_api import YouTubeTranscriptApi
from celery import shared_task
from .models import Summary
from django.shortcuts import get_object_or_404
from urllib.parse import urlparse, parse_qs

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
    obj.transcript=final
    obj.save()
    return final