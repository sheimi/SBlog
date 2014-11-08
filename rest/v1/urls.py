from django.conf.urls import url, include
from rest.v1.views import blogging
from django.http import Http404


def default_404(request):
    raise Http404


urlpatterns = [
    url(r'^/posts', include(blogging.urls)),
    url(r'^', default_404),
]
