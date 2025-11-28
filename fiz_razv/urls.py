from django.urls import path
from .views import rost_sozdanie
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('create_rost/',rost_sozdanie)
]
