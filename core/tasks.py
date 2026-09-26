from youtube_transcript_api import YouTubeTranscriptApi
from celery import shared_task
from .models import Summary
from django.shortcuts import get_object_or_404
from urllib.parse import urlparse, parse_qs
from ai.final_response import final_response

@shared_task
def TranscriptFetch(id):
    obj=get_object_or_404(Summary.objects.select_related('user'), id=id)
    
    # Robust YouTube ID extraction
    parsed_url = urlparse(obj.link)
    video_id = None
    if parsed_url.hostname == 'youtu.be':
        video_id = parsed_url.path[1:]
    elif parsed_url.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed_url.path == '/watch':
            video_id = parse_qs(parsed_url.query).get('v', [None])[0]
        elif parsed_url.path.startswith(('/embed/', '/v/')):
            video_id = parsed_url.path.split('/')[2]
    
    if not video_id:
        obj.summary = "Invalid YouTube URL provided."
        obj.save()
        return f"Invalid YouTube URL: {obj.link}"
        
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id)
        final=''
        for snippet in transcript:
            final=final+snippet.text
        response=final_response(transcript=final)
        obj.transcript=final
        obj.summary=response
        obj.save()
        return f"transcript and ai_response saved for id:{id}"
    except Exception as e:
        obj.summary = "Sorry, we couldn't process this video. It may not have subtitles available."
        obj.save()
        return f"Failed to process video {video_id}: {str(e)}"

# @shared_task
# def airesponsegeneration(transcript, id):
#     response=final_response(transcript=transcript)
#     data=get_object_or_404(Summary, id=id)
#     data.summary=response
#     data.save()
#     return f"ai_response saved for id:{id}"