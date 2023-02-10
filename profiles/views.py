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
