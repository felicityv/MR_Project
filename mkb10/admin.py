from django.contrib import admin

from .models import MKB10

@admin.register(MKB10)
class MKB10Admin(admin.ModelAdmin):
    list_display = ('code_mkb', 'diagnoz_mkb', 'mkb_klass')