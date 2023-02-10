from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
# ^ See cheat sheet for comments on import ^


class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        return Response(profiles)
