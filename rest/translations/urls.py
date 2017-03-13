from . import views, routers

router = routers.VideoRouter()
router.register(r'khan_academy_videos', views.KhanAcademyVideoViewSet)
router.register(r'youtube_videos', views.YoutubeVideoViewSet)
urlpatterns = router.urls
