import sys

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'partyapp.views.home', name='home'),
    # url(r'^partyapp/', include('partyapp.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^partys/', include('partyapp.events.urls')),
    url(r'^$/', include('partyapp.events.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
)


if 'runserver' in sys.argv:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True,
        }),
    )