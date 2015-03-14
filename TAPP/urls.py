from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^accounts/', include('allauth.urls')),
)

urlpatterns += patterns('backend.views',
    url(r'^$', 'index', name="index"),
    url(r'^profile$', 'profile', name="home"),
    url(r'^login$', 'login_page', name="login"),
    url(r'^process_login$', 'process_login'),
    url(r'^signup$', 'signup_page', name="signup"),
    url(r'^logout$', 'process_logout')
)



if settings.DEPLOY_MODE == "development":
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
