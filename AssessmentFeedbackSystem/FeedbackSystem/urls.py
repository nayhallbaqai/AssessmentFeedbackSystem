from django.conf.urls import url
from FeedbackSystem import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^course/$', views.course, name='course'),
]
