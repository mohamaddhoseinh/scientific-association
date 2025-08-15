from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError

class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ('workshop', 'کارگاه'),
        ('seminar', 'سمینار'),
        ('competition', 'مسابقه'),
        ('meeting', 'جلسه'),
        ('other', 'سایر'),
    )
    
    title = models.CharField(max_length=200, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    start_date = models.DateTimeField(verbose_name='تاریخ شروع')
    end_date = models.DateTimeField(verbose_name='تاریخ پایان')
    capacity = models.PositiveIntegerField(verbose_name='ظرفیت')
    registered_count = models.PositiveIntegerField(default=0, verbose_name='تعداد ثبت‌نام شده')
    location = models.CharField(max_length=200, verbose_name='مکان')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES, verbose_name='نوع رویداد')
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events', verbose_name='برگزارکننده')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'رویداد'
        verbose_name_plural = 'رویدادها'
        db_table = 'events'
        ordering = ['start_date']
    
    def __str__(self):
        return self.title
    
    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError('تاریخ پایان باید بعد از تاریخ شروع باشد')
    
    def is_full(self):
        return self.registered_count >= self.capacity
    
    def available_capacity(self):
        return self.capacity - self.registered_count
    
    def can_register(self):
        return self.is_active and not self.is_full() and self.start_date > timezone.now()


class EventRegistration(models.Model):
    STATUS_CHOICES = (
        ('registered', 'ثبت‌نام شده'),
        ('cancelled', 'لغو شده'),
        ('attended', 'حضور یافته'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_registrations', verbose_name='کاربر')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations', verbose_name='رویداد')
    registration_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ثبت‌نام')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered', verbose_name='وضعیت')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ایجاد')
    
    class Meta:
        verbose_name = 'ثبت‌نام رویداد'
        verbose_name_plural = 'ثبت‌نام‌های رویداد'
        db_table = 'event_registrations'
        unique_together = ['user', 'event']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"