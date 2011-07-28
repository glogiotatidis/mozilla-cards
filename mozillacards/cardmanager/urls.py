from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.conf import settings

urlpatterns = patterns(
    "cardmanager.views",
    url("^$", "index", name="index"),
    url("^generate/", "generate", name="generate"),
    )

if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r"%s(?P<path>.*)$" % settings.MEDIA_URL,
            "static.serve",
            {"document_root": settings.MEDIA_ROOT,})
    )

