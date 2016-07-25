from django.conf.urls import url

from . import views

app_name = 'waggle'
urlpatterns = [
            #url(r'^assessment/$', views.assessment, name='assessment'),
            url(r'^assessment/$', views.AssessmentView.as_view(), name='assessment'),
            ]
