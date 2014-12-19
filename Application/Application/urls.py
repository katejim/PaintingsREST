from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from django.conf.urls import url, include
from rest_framework import routers
import Application
from Application.Paintings import views

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^pictures$', views.PictureViewSet),
                       url(r'^pictures/(?P<stringType>\w+)$', views.PicturesTypedViewSet),
                       url(r'^tasks/(?P<stringType>\w+)/(?P<stringName>\w+)$', views.TasksPUTViewSet),
                       url(r'^tasks/(?P<taskID>\d+)/(?P<stringType>\w+)/(?P<stringName>\w+)$', views.TasksPOSTViewSet),
                       url(r'^tasks/(?P<taskID>\d+)/$', views.TasksDELETEViewSet),
                       url(r'^tasks/$', views.AllTasksViewSet),
                       url(r'^admin', include(admin.site.urls)),
                       url(r'.*', views.page_not_found_view),
)
