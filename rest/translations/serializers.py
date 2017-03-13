from .models import KhanAcademyVideo, YoutubeVideo
from rest_framework import serializers


class YoutubeVideoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = YoutubeVideo
        fields = ('url', 'title', 'description', 'duration', 'language')


class KhanAcademyVideoSerializer(serializers.HyperlinkedModelSerializer):
    youtube_url = serializers.CharField(source='youtube_video.url', required=False)
    self_link = serializers.HyperlinkedIdentityField(view_name='khanacademyvideo-detail')

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
