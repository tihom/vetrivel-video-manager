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
        # do not delete if youtube model is deleted
        on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def youtube_url(self):
        return self.youtube_video.url

class TaskQuerySet(models.QuerySet):
    def assigned(self):
        return self.filter(state='assigned')
    
    def completed(self):
        return self.filter(state='completed')


class Task(models.Model):
    TASK_TYPES = (
        ('subtitle', 'Subtitle translation'),
        ('subtitle_review', 'Subtitle review'),
        ('voiceover', 'Voiceover'),
        ('voiceover_review', 'Voiceover review')
    )
    STATES = (
        ('assigned', 'Assigned'),
        ('abandoned', 'Abandoned'),
        ('completed', 'Completed')
    )

    task_type = models.CharField(max_length=30, 
        choices=TASK_TYPES, db_index=True)
    state = models.CharField(max_length=30, 
        choices=STATES, db_index=True)
    language = models.CharField(max_length=3, 
        default='ta')
    comment = models.CharField(max_length=140, 
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video = models.ForeignKey(
        KhanAcademyVideo,
        on_delete=models.CASCADE)
    volunteer = models.ForeignKey(
        'volunteer.Volunteer',
        on_delete=models.CASCADE)

    objects = TaskQuerySet.as_manager()

