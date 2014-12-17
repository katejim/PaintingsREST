from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf.urls import url, include
from rest_framework import routers
import Application
from Application.Paintings import views

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'Application.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^pictures', views.PictureViewSet),
                       url(r'^admin/', include(admin.site.urls)),
)
