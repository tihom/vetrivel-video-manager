from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets

from .models import KhanAcademyVideo, YoutubeVideo
from .serializers import KhanAcademyVideoSerializer, YoutubeVideoSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the translations index.")


class KhanAcademyVideoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows khan academy videos to be viewed or edited.
    """
    queryset = KhanAcademyVideo.objects.all()
    serializer_class = KhanAcademyVideoSerializer


class YoutubeVideoViewSet(viewsets.ModelViewSet):
    queryset = YoutubeVideo.objects.all()
    serializer_class =  YoutubeVideoSerializer