from django.contrib import admin
from django.urls import path,include
from main.views import main
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main),
    # path('', include("fiz_razv.urls")),
    path('', include('patient.urls')),
    path('form/', include('study_form.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)