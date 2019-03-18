from django.contrib import admin
from django.contrib.admin import AdminSite

from .models.referencePDF import ReferencePDF
from .models.referenceWeb import ReferenceWeb


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('url', '_bibtex_reference',)
    fields = ('url', '_bibtex_reference',)
    # readonly_fields = ('_bibtex_reference',)

    def has_permission(self, request):
        """
        Removed check for is_staff.
        """
        return request.user.is_active


admin.site.register(ReferencePDF, ReferenceAdmin)
# user_admin_site = ReferenceAdmin()
