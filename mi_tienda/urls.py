from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from facturacion.views import InicioView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", InicioView.as_view(), name="home"),
    path("facturacion/", include("facturacion.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)