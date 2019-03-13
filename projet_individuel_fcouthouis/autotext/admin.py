from django.contrib import admin
from django.contrib.admin import AdminSite

from .models.referencePDF import ReferencePDF
from .models.referenceWeb import ReferenceWeb


admin.site.register(ReferencePDF)
admin.site.register(ReferenceWeb)
