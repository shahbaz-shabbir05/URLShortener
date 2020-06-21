from django.contrib import admin

from shortner.models import URL


# Register your models here.

@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'original_url', 'short_url', 'created_at')
