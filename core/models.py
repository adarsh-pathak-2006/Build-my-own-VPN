from django.db import models
from django.contrib.auth.models import User

class Summary(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    link=models.URLField()
    summary=models.TextField(null=True)
    time=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username

