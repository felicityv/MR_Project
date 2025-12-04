from django.contrib import admin
from .models import Patient
from .models import Rost
from .models import Ves
from .models import Imt
from .models import OsmotrPatient
from .models import Narushenie
from .models import FizicRazvit



admin.site.register(Patient)
admin.site.register(Rost)
admin.site.register(Ves)
admin.site.register(Imt)
admin.site.register(OsmotrPatient)
admin.site.register(Narushenie)
admin.site.register(FizicRazvit)