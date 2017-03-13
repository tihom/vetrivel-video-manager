from django.db import models


class YoutubeVideo(models.Model):
    url = models.CharField(db_index=True, 
        unique=True, max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration = models.CharField(max_length=20,
        blank=True)
    language = models.CharField(max_length=20)

    def __str__(self):
        return self.url


class KhanAcademyVideo(models.Model):
    sno = models.CharField(max_length=255)
    title = models.CharField(db_index=True, max_length=255)
    domain = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    tutorial = models.CharField(max_length=255)
    priority = models.IntegerField(blank=True, null=True)
    # has one youtube video doc
    youtube_video = models.ForeignKey(YoutubeVideo,
        on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
