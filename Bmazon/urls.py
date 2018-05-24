from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^book/', include('book.urls', namespace='book')),
    url(r'^manager/', include('manager.urls', namespace='manager')),
]
urlpatterns += staticfiles_urlpatterns()
