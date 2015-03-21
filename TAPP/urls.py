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

urlpatterns += patterns('backend.api',
    url(r'^api/v1/get_user_info$', 'get_user_info'),
    url(r'^api/v1/login$', 'user_login'),
    url(r'^api/v1/logout$', 'user_logout'),
    url(r'^api/v1/force_logout$', 'force_logout'),
    url(r'^api/v1/is_logged_in$', 'is_logged_in'),
    url(r'^api/v1/register$', 'user_register'),
)



if settings.DEPLOY_MODE == "development":
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
