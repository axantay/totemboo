from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class GalleryTabular(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'quantity', 'price', 'created_at', 'size', 'colour', 'get_photo')
    list_editable = ('price', 'category', 'quantity', 'size', 'colour')
    list_display_links = ('pk', 'title')
    inlines = [GalleryTabular]
    prepopulated_fields = {'slug': ('title',)}

    def get_photo(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
            except:
                return '-'
        else:
            return '-'


@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = ('pk', 'title')
    prepopulated_fields = {'slug': ('title',)}
