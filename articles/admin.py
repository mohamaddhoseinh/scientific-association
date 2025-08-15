from django.contrib import admin
from django.utils import timezone  # این خط اضافه شد
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'submission_date', 'reviewed_date')
    list_filter = ('status', 'category', 'submission_date')
    search_fields = ('title', 'abstract', 'author__username')
    ordering = ('-submission_date',)
    raw_id_fields = ('author', 'reviewer')
    
    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.status in ['approved', 'rejected']:
            obj.reviewer = request.user
            obj.reviewed_date = timezone.now()
        super().save_model(request, obj, form, change)