from django.contrib import admin
from django.contrib.admin import AdminSite

from .models.webography import Webography
from .models.referencePDF import ReferencePDF
from .models.referenceWeb import ReferenceWeb


# class ReferenceAdmin(admin.ModelAdmin):
#     list_display = ('url', '_bibtex_reference', 'webography')
#     fields = ('url', '_bibtex_reference',)
#     readonly_fields = ('_bibtex_reference',)


admin.site.register(Webography)
admin.site.register(ReferencePDF)
admin.site.register(ReferenceWeb)
