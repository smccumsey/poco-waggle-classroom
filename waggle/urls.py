from django.conf.urls import url, include

from . import views

app_name = 'waggle'
urlpatterns = [
            #url(r'^assessment/$', views.assessment, name='assessment'),
            url(r'^assessment/$', views.AssessmentView.as_view(), name='assessment'),
            url(r'^login/$', views.LoginView.as_view(), name='login'),
            url('', include('social.apps.django_app.urls', namespace='social'))
            ]
