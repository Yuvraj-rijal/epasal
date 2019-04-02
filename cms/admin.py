from django.contrib import admin

from .models import TopBanner, BottomBanner, Menu

# Register your models here.

admin.site.register(TopBanner)
admin.site.register(BottomBanner)
admin.site.register(Menu)