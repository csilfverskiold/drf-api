from rest_framework.decorators import api_view
from rest_framework.response import Response

"""In drf_api, I'll create a views.py file
and inside, I'll import the api_view  decorator and the Response class,
as we'll write a very simple function based view,  similar to what we did
at the very beginning. I'll create the root_route and return  a Response
with a custom message. It can be whatever you want. Don't forget to import
it into the drf_api/urls.py file and add it to the urlpatterns list."""


@api_view()
def root_route(request):
    return Response({
        "message": "Welcome to my drf API!"
    })
