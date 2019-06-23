from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class YoutubeVideo(models.Model):
    vid = models.CharField(primary_key=True, max_length=100, db_index=True)
    title = models.CharField(max_length=255)
    author_name = models.CharField(max_length=64, default='Youtuber')
    author_url = models.CharField(max_length=64, null=True)
    description = models.TextField(default="Video description here.")
    shared_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shared_videos')
    shared_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "youtube_video"

    @property
    def description_text(self):
        if self.author_url:
            return 'Published by <a href="{}" target="_blank"><b>{}</b></a>.'.format(
                self.author_url, self.author_name)
        return 'Published by <b>{}</b>.'.format(self.author_name)
