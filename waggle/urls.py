from django.conf.urls import url, include
from django.http import HttpResponse

from . import views

app_name = 'waggle'
urlpatterns = [
            url(r'^assessment/$', views.AssessmentView.as_view(), name='assessment'),
            url(r'^tokensignin/$', views.VerifyToken.as_view(), name='tokensignin'),
            url(r'^login/$', views.LoginView.as_view(), name='login'),
            url(r'^google8a43fbed4f8a62b6\.html$', lambda r: HttpResponse("google-site-verification: google8a43fbed4f8a62b6.html", content_type="text/plain")),
            url('', include('social.apps.django_app.urls', namespace='social'))
            ]
