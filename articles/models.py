from django.db import models
from django.conf import settings
from django.utils import timezone

class Article(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار بررسی'),
        ('approved', 'تایید شده'),
        ('rejected', 'رد شده'),
        ('revision', 'نیاز به اصلاح'),
    )
    
    title = models.CharField(max_length=200, verbose_name='عنوان')
    abstract = models.TextField(verbose_name='چکیده')
    file = models.FileField(upload_to='articles/', verbose_name='فایل مقاله')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='articles', verbose_name='نویسنده')
    category = models.ForeignKey('news.Category', on_delete=models.SET_NULL, null=True, related_name='articles', verbose_name='دسته‌بندی')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    review_comment = models.TextField(blank=True, verbose_name='نظر داور')
    submission_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ارسال')
    reviewed_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ بررسی')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_articles', verbose_name='داور')
    
    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        db_table = 'articles'
        ordering = ['-submission_date']
    
    def __str__(self):
        return self.title