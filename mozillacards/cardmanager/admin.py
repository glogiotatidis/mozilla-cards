from django.contrib import admin

from cardmanager.models import Template

class TemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "default", "updated")
    search_fields = ("name", )

admin.site.register(Template, TemplateAdmin)
