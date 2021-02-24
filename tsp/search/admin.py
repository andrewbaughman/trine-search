from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(links)
admin.site.register(page_results)
admin.site.register(keywords)
admin.site.register(page)