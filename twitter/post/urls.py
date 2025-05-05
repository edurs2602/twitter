from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, all)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/all/', all, name='post-all'),

    path('posts/<uuid:pk>/like/', PostViewSet.as_view({'post': 'like'}), name='post-like'),
    path('posts/<uuid:pk>/unlike/', PostViewSet.as_view({'post': 'unlike'}), name='post-unlike'),
]
