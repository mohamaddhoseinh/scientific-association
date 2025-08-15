from django.db import models
from django.utils import timezone
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام دسته‌بندی')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        db_table = 'categories'
    
    def __str__(self):
        return self.name
    
class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    content = models.TextField(verbose_name='محتوا')
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name='تصویر')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news', verbose_name='نویسنده')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='news', verbose_name='دسته‌بندی')
    is_published = models.BooleanField(default=False, verbose_name='منتشر شده')
    publish_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ انتشار')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')
    
    class Meta:
        verbose_name = 'خبر'
        verbose_name_plural = 'اخبار'
        db_table = 'news'
        ordering = ['-publish_date', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.is_published and not self.publish_date:
            self.publish_date = timezone.now()
        super().save(*args, **kwargs)