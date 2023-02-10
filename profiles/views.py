from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
# ^ See cheat sheet for comments on import ^


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

# "Our serializer has taken the Python  data and converted it
# into JSON, which is ready for the front end content to use!"


class ProfileDetail(APIView):
    serializer_class = ProfileSerializer
# "If we explicitly set the serializer_class attribute  on our
# ProfileDetail view, the rest framework will automatically
# render a form for us, based on  the fields we defined in our
# ProfileSerializer."

    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    # GET
    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    # PUT
    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
