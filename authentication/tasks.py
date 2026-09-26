from celery import shared_task
from django.core.cache import cache
from config.cache_keys import otpCacheKey
import requests
from django.conf import settings

@shared_task
def OTPCreation(id, email):
    response=requests.post(settings.OTP_SERVICE_URL, json={"email":email})
    response.raise_for_status()
    cache.set(otpCacheKey(id=id), response.json().get("data", {}).get("otp"), timeout=500)
    return f"otp sent to {email} otp_data here: {response.json()}"