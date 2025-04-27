from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User
from .serializers import RegisterSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset      = User.objects.all()
    lookup_field  = 'uuid'

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        payload = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
        return Response(payload, status=status.HTTP_201_CREATED)
