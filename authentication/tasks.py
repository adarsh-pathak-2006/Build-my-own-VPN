from celery import shared_task
from django.core.cache import cache
import random
import time
from config.cache_keys import otpCacheKey

@shared_task
def OTPCreation(id, email):
    time.sleep(5)
    otp=str(random.randint(11111111, 99999999))
    cache.set(otpCacheKey(id=id), otp, timeout=500)
    return f"otp sent to {email} otp:{otp}"