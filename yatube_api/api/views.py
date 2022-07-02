from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from posts.models import Group, Post
from .permissions import ForAuthorOthersAuthorizedOnlyRead
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [ForAuthorOthersAuthorizedOnlyRead]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ForAuthorOthersAuthorizedOnlyRead]

    def get_object_post_or_404(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, post=self.get_object_post_or_404())

    def get_queryset(self):
        return self.get_object_post_or_404().comments.all()
