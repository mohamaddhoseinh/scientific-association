import os
import django

# تنظیم Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from news.models import Category, News
from events.models import Event, EventRegistration
from articles.models import Article
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def create_sample_data():
    print("شروع ساخت داده‌های نمونه...")
    
    # پاک کردن داده‌های قبلی
    print("پاک کردن داده‌های قبلی...")
    User.objects.filter(is_superuser=False).delete()
    Category.objects.all().delete()
    News.objects.all().delete()
    Event.objects.all().delete()
    Article.objects.all().delete()
    
    # ساخت کاربران
    print("ساخت کاربران...")
    
    # کاربر عادی
    user1 = User.objects.create_user(
        username='user1',
        email='user1@example.com',
        password='testpass123',
        first_name='علی',
        last_name='احمدی',
        phone='09123456789',
        student_id='9912345001',
        role='user'
    )
    
    # عضو انجمن
    member1 = User.objects.create_user(
        username='member1',
        email='member1@example.com',
        password='testpass123',
        first_name='سارا',
        last_name='محمدی',
        phone='09123456790',
        student_id='9912345002',
        role='member'
    )
    
    # مدیر
    admin1 = User.objects.create_user(
        username='admin1',
        email='admin1@example.com',
        password='testpass123',
        first_name='محمد',
        last_name='رضایی',
        phone='09123456791',
        student_id='9912345003',
        role='admin'
    )
    
    # ساخت دسته‌بندی‌ها
    print("ساخت دسته‌بندی‌ها...")
    cat1 = Category.objects.create(
        name='فناوری',
        description='اخبار و مقالات مربوط به فناوری'
    )
    
    cat2 = Category.objects.create(
        name='علمی',
        description='اخبار و مقالات علمی'
    )
    
    cat3 = Category.objects.create(
        name='آموزشی',
        description='محتوای آموزشی'
    )
    
    # ساخت اخبار
    print("ساخت اخبار...")
    news1 = News.objects.create(
        title='برگزاری کارگاه برنامه‌نویسی پایتون',
        content='کارگاه برنامه‌نویسی پایتون برای مبتدیان برگزار خواهد شد.',
        author=admin1,
        category=cat3,
        is_published=True,
        publish_date=timezone.now()
    )
    
    news2 = News.objects.create(
        title='اعلام نتایج مسابقه برنامه‌نویسی',
        content='نتایج مسابقه برنامه‌نویسی اعلام شد.',
        author=member1,
        category=cat1,
        is_published=True,
        publish_date=timezone.now()
    )
    
    # ساخت رویدادها
    print("ساخت رویدادها...")
    event1 = Event.objects.create(
        title='کارگاه Django',
        description='آموزش فریمورک Django برای توسعه وب',
        start_date=timezone.now() + timedelta(days=7),
        end_date=timezone.now() + timedelta(days=7, hours=3),
        capacity=30,
        location='سالن کنفرانس دانشکده',
        event_type='workshop',
        organizer=member1
    )
    
    event2 = Event.objects.create(
        title='سمینار هوش مصنوعی',
        description='بررسی آخرین پیشرفت‌های هوش مصنوعی',
        start_date=timezone.now() + timedelta(days=14),
        end_date=timezone.now() + timedelta(days=14, hours=2),
        capacity=50,
        location='آمفی تئاتر مرکزی',
        event_type='seminar',
        organizer=admin1
    )
    
    # ثبت‌نام در رویداد
    EventRegistration.objects.create(
        user=user1,
        event=event1,
        status='registered'
    )
    event1.registered_count = 1
    event1.save()
    
    # ساخت مقالات
    print("ساخت مقالات...")
    article1 = Article.objects.create(
        title='بررسی الگوریتم‌های یادگیری ماشین',
        abstract='این مقاله به بررسی انواع الگوریتم‌های یادگیری ماشین می‌پردازد.',
        author=user1,
        category=cat1,
        status='pending'
    )
    
    article2 = Article.objects.create(
        title='کاربرد Django در توسعه وب',
        abstract='بررسی مزایا و کاربردهای فریمورک Django',
        author=member1,
        category=cat2,
        status='approved',
        reviewer=admin1,
        reviewed_date=timezone.now()
    )
    
    print("داده‌های نمونه با موفقیت ایجاد شدند!")
    print(f"کاربران: {User.objects.count()}")
    print(f"دسته‌بندی‌ها: {Category.objects.count()}")
    print(f"اخبار: {News.objects.count()}")
    print(f"رویدادها: {Event.objects.count()}")
    print(f"مقالات: {Article.objects.count()}")

if __name__ == '__main__':
    create_sample_data()