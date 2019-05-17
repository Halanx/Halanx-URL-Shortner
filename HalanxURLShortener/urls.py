from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from utility.environments import DEVELOPMENT

urlpatterns = [
    url(r'^api/', include('shortener.api.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('shortener.urls')),
]

if settings.DEBUG and settings.ENVIRONMENT == DEVELOPMENT:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
