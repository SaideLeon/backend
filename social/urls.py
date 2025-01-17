# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet, LikeViewSet, ShareViewSet

router = DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'shares', ShareViewSet)

urlpatterns = [
    path('', include(router.urls)),
]