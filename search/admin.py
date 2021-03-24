from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(links)
admin.site.register(keywords)
admin.site.register(page)
admin.site.register(edges)