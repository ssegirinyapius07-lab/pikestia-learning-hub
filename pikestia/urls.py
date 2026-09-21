from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.core.urls')),
    path('', include('apps.subjects.urls')),
    path('', include('apps.learning.urls')),
    path('', include('apps.practice.urls')),
    path('', include('apps.opportunities.urls')),
    path('', include('apps.bookmarks.urls')),
    path('', include('apps.news.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = 'apps.core.views.error_400'
handler401 = 'apps.core.views.error_401'
handler403 = 'apps.core.views.error_403'
handler404 = 'apps.core.views.error_404'
handler429 = 'apps.core.views.error_429'
handler500 = 'apps.core.views.error_500'
