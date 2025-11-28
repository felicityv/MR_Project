from django.contrib import admin
from .models import Patient
from .models import Rost
from .models import Ves
from .models import Imt

admin.site.register(Patient)
admin.site.register(Rost)
admin.site.register(Ves)
admin.site.register(Imt)