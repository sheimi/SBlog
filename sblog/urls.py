from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/?', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api/v1', include('rest.v1.urls', namespace='rest.v1')),
    url(r'^', include('core.urls', namespace='genie')),
)
