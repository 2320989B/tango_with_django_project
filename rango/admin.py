from django.contrib import admin
from rango.models import Category, Page


# Customise the Category Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'views', 'likes', 'slug')


# Customise the Page Admin Interface
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'views')


# Registration
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
