from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """

    """To be able to sort these fields,  first we will have to define them,
    using the 'annotate' function  on the List view queryset.
    Let's go then to profiles' views.py  file. First, we'll import the Count
    class to count model instances. We'll also need  rest_framework's filters
    to order our profiles. Now we are going to remove the dot-all function
    from our queryset and modify it using the annotate function instead.
    The annotate function allows us to define extra fields to be added to the
    queryset. In our case, we'll add fields to work  out how many posts and
    followers a user has, and how many other users they're following."""
    # queryset = Profile.objects.all()
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    """Next, we'll need to create our filters. To make these fields sortable,
    I'll set the filter_backends attribute to OrderingFilter.
    I'll also need to set the ordering_fields  to the fields we just annotated,
    namely posts, followers and following count."""
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    ordering_fields = [
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
