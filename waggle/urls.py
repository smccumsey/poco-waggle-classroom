from django.conf.urls import url, include
from django.http import HttpResponse
#from django.contrib.auth import views as auth_views
from . import views

app_name = 'waggle'
urlpatterns = [
            url(r'^assessment/$', views.AssessmentView.as_view(), name='assessment'),
            #url(r'^login/$', auth_views.login, {'template_name': 'waggle/login.html'}, name='login'),
            url(r'^login/$', views.LoginView.as_view(), name='login'),
            url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
            url(r'^profile/(?P<pk>)?/$', views.ProfileView.as_view(), name='profile'),
            url(r'^profile/(?P<pk>[a-zA-Z]+)?/$', views.ProfileView.as_view(), name='profile'),
            url(r'^profile/(?P<pk>[0-9]+)?/$', views.ProfileView.as_view(), name='profile'),
            url(r'^google8a43fbed4f8a62b6\.html$', lambda r: HttpResponse("google-site-verification: google8a43fbed4f8a62b6.html", content_type="text/plain")),
            #url('', include('social.apps.django_app.urls', namespace='social')),
            ]
