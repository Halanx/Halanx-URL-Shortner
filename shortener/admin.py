from django.contrib import admin

from .models import Url


@admin.register(Url)
class UrlModelAdmin(admin.ModelAdmin):
    list_display = ('short', )
    search_fields = ('short', )
