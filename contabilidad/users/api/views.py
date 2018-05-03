from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from .serializers import CommentSerializer


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class CommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, *args, **kwargs):
        user = self.request.user
        return user.profile

    def get(self, request, *args, **kwargs):
        object = self.get_object(*args, **kwargs)
        serializer = CommentSerializer(object.comments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            object = self.get_object(*args, **kwargs)
            serializer = CommentSerializer(object.comments, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
