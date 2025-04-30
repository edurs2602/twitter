from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from core.permissions import IsOwnerOrReadOnly
from ..models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user__username=username)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()

        if post.likes.filter(id=request.user.id).exists():
            return Response({'error': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        post.likes.add(request.user)
        post.save()

        return Response({'message': 'Post liked successfully!'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        post = self.get_object()

        if not post.likes.filter(id=request.user.id).exists():
            return Response({'error': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        post.likes.remove(request.user)
        post.save()

        return Response({'message': 'Post unliked successfully!'}, status=status.HTTP_200_OK)
