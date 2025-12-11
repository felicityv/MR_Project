from django.contrib import admin
from .models import Rost
from .models import Ves
from .models import Imt
from .models import Narushenie
from .models import FizicRazvit

admin.site.register(Rost)
admin.site.register(Ves)
admin.site.register(Imt)
admin.site.register(Narushenie)
admin.site.register(FizicRazvit)