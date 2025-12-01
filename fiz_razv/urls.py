from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import patient_info
# from .views import imt_sozdanie
from . import views 
urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('create_rost/',imt_sozdanie)
    path('patients/', views.patient_info, name='patient_list'),
    path('patients/<int:pk>/', views.patient_info, name='patient_detail'),
    path('main/', patient_info),
]