from django.contrib import admin
from .models import Product
from django.utils.html import format_html



class ProductAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'quantite', 'image_tag')  # ajoute image_tag

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />'.format(obj.image.url))
        return "-"
    image_tag.short_description = 'Image'

admin.site.register(Product, ProductAdmin)