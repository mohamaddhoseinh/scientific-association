from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('نام کاربری الزامی است')
        if not email:
            raise ValueError('ایمیل الزامی است')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('user', 'کاربر عادی'),
        ('member', 'عضو انجمن'),
        ('admin', 'مدیر'),
    )
    
    username = models.CharField(max_length=50, unique=True, verbose_name='نام کاربری')
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    first_name = models.CharField(max_length=50, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=15, blank=True, verbose_name='تلفن')
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name='شماره دانشجویی')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', verbose_name='نقش')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_staff = models.BooleanField(default=False, verbose_name='کارمند')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ثبت نام')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        db_table = 'users'
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_member(self):
        return self.role in ['member', 'admin']