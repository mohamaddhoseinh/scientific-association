import os
import django
from django.conf import settings

# تنظیم Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

try:
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    print("✅ اتصال به دیتابیس موفقیت‌آمیز بود!")
except Exception as e:
    print(f"❌ خطا در اتصال به دیتابیس: {e}")