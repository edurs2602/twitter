import uuid
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import Follow
from .serializers import FollowSerializer

User = get_user_model()

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        try:
            user_to_follow = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user_to_follow == request.user:
            return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        if Follow.objects.filter(user=request.user, following_user=user_to_follow).exists():
            return Response({'error': 'You are already following this user.'}, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.create(user=request.user, following_user=user_to_follow)
        return Response({'message': f'Now following {user_to_follow.username}.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        try:
            user_to_unfollow = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user_to_unfollow == request.user:
            return Response({'error': 'You cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.filter(user=request.user, following_user=user_to_unfollow)
        if not follow.exists():
            return Response({'error': 'You are not following this user.'}, status=status.HTTP_400_BAD_REQUEST)

        follow.delete()
        return Response({'message': f'You have unfollowed {user_to_unfollow.username}.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def followers_count(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        followers_count = Follow.objects.filter(following_user=user).count()
        return Response({'followers_count': followers_count}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def following_count(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        following_count = Follow.objects.filter(user=user).count()
        return Response({'following_count': following_count}, status=status.HTTP_200_OK)
