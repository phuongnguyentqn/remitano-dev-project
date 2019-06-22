from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class YoutubeVideo(models.Model):
    vid = models.CharField(primary_key=True, max_length=100, db_index=True)
    title = models.CharField(max_length=255)
    html = models.TextField()
    shared_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shared_videos')
    shared_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "youtube_video"
