from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


"""...As the logic inside the Post views is the same, wouldn't it be handy if
we didn't have to write the same methods, such as get, post, put and
delete over and over again? This brings us to generic views.
The Django Documentation states that generic views were developed as
a shortcut for common usage patterns. What this means is that we can achieve
all the same functionality of the get, post, put and other class based
view methods without having to repeat ourselves so much."""


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
