from django.contrib import admin
from django.utils import timezone
from .models import Category, News

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'publish_date', 'created_at')
    list_filter = ('is_published', 'category', 'created_at', 'publish_date')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    raw_id_fields = ('author',)
    
    def save_model(self, request, obj, form, change):
        if not change:  # اگر جدید است
            obj.author = request.user
        super().save_model(request, obj, form, change)