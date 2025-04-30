from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import FollowViewSet

router = DefaultRouter()
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('follow/<uuid:pk>/follow/', FollowViewSet.as_view({'post': 'follow'}), name='follow_user'),
    path('follow/<uuid:pk>/unfollow/', FollowViewSet.as_view({'post': 'unfollow'}), name='unfollow_user'),
    path('follow/<uuid:pk>/followers_count/', FollowViewSet.as_view({'get': 'followers_count'}), name='count_followers'),
    path('follow/<uuid:pk>/following_count/', FollowViewSet.as_view({'get': 'following_count'}), name='count_following'),

    path('', include(router.urls)),
]
