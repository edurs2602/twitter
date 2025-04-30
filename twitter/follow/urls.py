from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .api.views import FollowViewSet

router = DefaultRouter()
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    re_path(r'^follow/(?P<pk>[0-9a-fA-F-]{36})/follow/$', FollowViewSet.as_view({'post': 'follow'}),
            name='follow_user'),
    re_path(r'^follow/(?P<pk>[0-9a-fA-F-]{36})/unfollow/$', FollowViewSet.as_view({'post': 'unfollow'}),
            name='unfollow_user'),
    re_path(r'^follow/(?P<pk>[0-9a-fA-F-]{36})/followers_count/$', FollowViewSet.as_view({'get': 'followers_count'}),
            name='count_followers'),
    re_path(r'^follow/(?P<pk>[0-9a-fA-F-]{36})/following_count/$', FollowViewSet.as_view({'get': 'following_count'}),
            name='count_following'),

    path('', include(router.urls)),
]
