from django.conf.urls.defaults import url, patterns, include
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

handler404 = "project.views.page_not_found"
handler500 = "project.views.server_error"

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/setlang/$', 'django.views.i18n.set_language'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
    ) + urlpatterns