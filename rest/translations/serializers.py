from .models import KhanAcademyVideo, YoutubeVideo, Task
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

class TaskSerializer(serializers.HyperlinkedModelSerializer):

    task = serializers.ChoiceField(source='task_type', 
        choices=Task.TASK_TYPES)
    state = serializers.ChoiceField(source='state',
        choices=Task.STATES)
    startDate = serializers.DateTimeField(source='created_at')
    video_id = serializers.IntegerField(source='video.id', 
        validators=[UniqueValidator(queryset=Task.objects.assigned())])
    video_title = serializers.CharField(source='video.title', 
        read_only=True)
    video_url = serializers.CharField(source='video.youtube_url',
        read_only=True)
    owner_id = serializers.IntegerField(source='volunteer.user.id', 
        validators=[UniqueValidator(queryset=Task.objects.assigned())])
    owner_name = serializers.CharField(source='volunteer.name',
        read_only=True)
    owner_email = serializers.CharField(source='volunteer.email',
        read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'task', 'state', 'startDate', 
            'video_id', 'video_title', 'video_url',
            'owner_id', 'owner_name', 'owner_email')

class YoutubeVideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = YoutubeVideo
        fields = ('url', 'title', 'description', 'duration', 'language')


class KhanAcademyVideoSerializer(serializers.HyperlinkedModelSerializer):
    youtube_url = serializers.CharField(source='youtube_video.url', 
        required=False)
    self_link = serializers.HyperlinkedIdentityField(
        view_name='khanacademyvideo-detail')

    class Meta:
        model = KhanAcademyVideo
        fields = ('sno', 'title', 'domain', 'subject', 'topic',
        	'tutorial', 'priority', 'self_link', 'youtube_url',)
        extra_kwargs = {
            "tutorial": {"required": False}
        }

#     def create(self, validated_data):
#         video_meta_data = validated_data.pop('video_meta', None)
#         if video_meta_data is not None:
#             video_meta = VideoMeta.objects.create(**video_meta_data)
#             validated_data.update({'video_meta': video_meta})

#         original_video = OriginalVideo.objects.create(**validated_data)
#         return original_video

#     def update(self, instance, validated_data):
#         video_meta_data = validated_data.pop('video_meta', None)
#         if video_meta_data is not None:
#             if hasattr(instance, 'video_meta'):
#                 video_meta = instance.video_meta
#                 super(OriginalVideoSerializer, self).update(video_meta, video_meta_data)
#             else:
#                 video_meta = VideoMeta.objects.create(**video_meta_data)
#                 instance.video_meta = video_meta

#         return super(OriginalVideoSerializer, self).update(instance, validated_data)
