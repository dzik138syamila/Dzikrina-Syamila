# blog/admin.py

from django.contrib import admin
from .models import Category, Page, Blog

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'slug')
    prepopulated_fields = {'slug': ('category',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_date', 'published_date')
    list_filter = ('category', 'status', 'created_date', 'published_date')
    search_fields = ('title', 'author', 'content')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Blog, BlogAdmin)
