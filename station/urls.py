from django.conf import settings
from django.conf.urls import patterns, include, url
from .views import (MenuView, StatusView, LogView, ActivityCreateView,
                    PuzzleView, RepairView, CommunicationView, AdminView)

urlpatterns = patterns('',
    url(r'^(?P<pk>[0-9]+)/$', MenuView.as_view(), name='home'),
    url(r'^(?P<pk>[0-9]+)/status/$', StatusView.as_view(), name='status'),
    url(r'^(?P<pk>[0-9]+)/logs/$', LogView.as_view(), name='logs'),
    url(r'^(?P<pk>[0-9]+)/communications/$', CommunicationView.as_view(), name='comms'),
    url(r'^(?P<pk>[0-9]+)/repairs/$', RepairView.as_view(), name='repairs'),
    url(r'^(?P<pk>[0-9]+)/admin/$', AdminView.as_view(), name='admin'),

    url(r'^(?P<pk>[0-9]+)/activity/new/$', ActivityCreateView.as_view(), name='new-activity'),

    url(r'^p/(?P<pk>[0-9]+)/$', PuzzleView.as_view(), name='puzzle'),
)

if getattr(settings, 'DEBUG', False):
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
