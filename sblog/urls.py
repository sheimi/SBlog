from django.conf.urls import include, url
from django.contrib import admin

from sblog import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'sblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1', include(views.api_urls)),
    url(r'^', 'sblog.views.home'),
]
