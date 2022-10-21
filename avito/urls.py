from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ads.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('', include('ads.urls')),
    path('', include('user.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
