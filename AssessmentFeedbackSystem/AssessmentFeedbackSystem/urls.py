from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'AssessmentFeedbackSystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('FeedbackSystem.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
]
