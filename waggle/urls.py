from django.conf.urls import url, include
from django.http import HttpResponse
from . import views

app_name = 'waggle'
urlpatterns = [
            url(r'^login/$', views.LoginView.as_view(), name='login'),
            url(r'^google8a43fbed4f8a62b6\.html$', lambda r: HttpResponse("google-site-verification: google8a43fbed4f8a62b6.html", content_type="text/plain")),
            url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
            url(r'^profile/(?P<pk>)?/$', views.ProfileView.as_view(), name='profile'),
            url(r'^profile/(?P<pk>[a-zA-Z]+)?/$', views.ProfileView.as_view(), name='profile'),
            url(r'^profile/(?P<pk>[0-9]+)?/$', views.ProfileView.as_view(), name='profile'),
            url(r'^menu/(?P<pk>[0-9]+)/(?P<course>[a-zA-Z\-]+)/$', views.MenuView.as_view(), name='menu'),
            url(r'^assessment/$', views.AssessmentView.as_view(), name='assessment'),
           # url(r'^assessment/(?P<pk>[0-9]+)/(?P<course>[a-zA-Z\-]+)/(?P<module>[a-zA-Z0-9\-]+)/$', views.AssessmentView.as_view(), name='assessment'),
            ]
