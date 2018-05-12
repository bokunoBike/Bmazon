from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^book/', include('book.urls', namespace='book')),
    url(r'^manager/', include('manager.urls', namespace='manager')),
]
