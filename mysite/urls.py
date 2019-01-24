"""mysite URL configuration"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(url='/static/menu/favicon.ico/', permanent=True)

urlpatterns = [
    path('favicon.ico/', favicon_view),
    path('admin/', admin.site.urls),
    path('', include('menu.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
