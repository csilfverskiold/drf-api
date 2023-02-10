from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class PostList(APIView):
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(
            posts, many=True, context={'request': request}
        )
        return Response(serializer.data)

    """To actually have posts appear, we have to  make it possible for our
    users to create them. To achieve that, we have to define the  post method
    inside the PostList view. Inside it, we'll need to: deserialize the
    incoming request data, if the data is valid, save the post and associate
    it with the current user, return the post with the 201 CREATED HTTP code.
    In case the data is invalid, return the  errors together with the
    400 BAD REQUEST code. So, inside the post method, I'll deserialize the post
    data, passing in whatever the user sends in the request and the request
    itself in the context object. If the is_valid() method doesn't throw,
    I'll call the save method on the serializer and  pass in the user that is
    making the request. We'll be returning serialized data with  the 201 status
    if the serializer is valid, and we'll return serializer errors with the
    400 status otherwise. To have a nice create post form rendered in the
    preview window, let's also set the serializer_class attribute to
    PostSerializer on our PostList class."""
    # Below v

    def post(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class PostDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostSerializer

    def get_object(self, pk):
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, post)
            return post
        except Post.DoesNotExist:
            raise Http404

    # GET
    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, context={'request': request}
        )
        return Response(serializer.data)

    # PUT
    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(
            post, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE
    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
