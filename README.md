# Minggu 4 (Django Framework & ORM)

Core LMS Models: User (custom, role ADMIN/LECTURER/STUDENT), Course, Lesson,
Enrollment, Assignment, Submission. Stack: Django 5.2, PostgreSQL 17, Docker Compose.

## Menjalankan

1. Buat file `.env` di root project:
   ```
   DB_NAME=lms_db
   DB_USER=lms_user
   DB_PASSWORD=lms_password
   ```
2. Build dan jalankan:
   ```
   docker compose up -d --build
   docker compose exec app python manage.py migrate
   docker compose exec app python manage.py createsuperuser
   docker compose exec app python manage.py seed_demo
   ```
3. Buka http://localhost:8000/admin/

## Test

```
docker compose exec app python manage.py test catalog
```

## Catatan

- `.env` tidak di-commit; buat sendiri sesuai contoh di atas.
- `seed_demo` bersifat idempotent (aman dijalankan berulang).


# Minggu 5 (Optimasi Performa Database)

Project ini berisi implementasi dan pengujian optimasi performa database PostgreSQL pada aplikasi **Simple LMS** menggunakan Django ORM dan Docker Compose.

## 🛠️ Langkah-Langkah Pengerjaan & Pengujian

1. Menyiapkan Dataset Performa (10.000+ Records)
   Jalankan dua perintah *management command* berikut untuk mengenerate dataset simulasi secara otomatis:
   ```bash
   # Generate 10.000 data Course berkode PERF
     docker compose exec app python manage.py generate_performance_data

   # Generate data relasi (5 Lecturer, 50 Student, Enrollment, Lesson, Assignment, Submission)
     docker compose exec app python manage.py generate_relationship_data

2. Pengujian N+1 Query pada Django Shell
   `docker compose exec app python manage.py shell`

   A. Uji Course + Lecturer (N+1 vs select_related)
      BEFORE (Tanpa Optimasi - 101 Query):
      `from django.db import connection; from django.test.utils import CaptureQueriesContext; from catalog.models import Course; ctx = CaptureQueriesContext(connection); ctx.__enter__(); res = [(c.title, c.lecturer.username) for c in Course.objects.filter(code__startswith="PERF").order_by("code")[:100]]; ctx.__exit__(None, None, None); print("Jumlah Query SQL (BEFORE):", len(ctx.captured_queries))`

      AFTER (Dengan select_related - 1 Query):
      `from django.db import connection; from django.test.utils import CaptureQueriesContext; from catalog.models import Course; ctx = CaptureQueriesContext(connection); ctx.__enter__(); res = [(c.title, c.lecturer.username) for c in Course.objects.filter(code__startswith="PERF").order_by("code").select_related("lecturer")[:100]]; ctx.__exit__(None, None, None); print("Jumlah Query SQL (AFTER):", len(ctx.captured_queries))`

   B. Uji Course + Lesson (N+1 vs prefetch_related)
      BEFORE (Tanpa Optimasi - 51 Query):
      `from django.db import connection; from django.test.utils import CaptureQueriesContext; from catalog.models import Course; ctx = CaptureQueriesContext(connection); ctx.__enter__(); [ [l.title for l in c.lessons.all()] for c in Course.objects.filter(code__startswith="PERF").order_by("code")[:50] ]; ctx.__exit__(None, None, None); print("Jumlah Query SQL (BEFORE):", len(ctx.captured_queries))`

      AFTER (Dengan prefetch_related - 2 Query):
      `from django.db import connection; from django.test.utils import CaptureQueriesContext; from catalog.models import Course; ctx = CaptureQueriesContext(connection); ctx.__enter__(); [ [l.title for l in c.lessons.all()] for c in Course.objects.filter(code__startswith="PERF").order_by("code").prefetch_related("lessons")[:50] ]; ctx.__exit__(None, None, None); print("Jumlah Query SQL (AFTER):", len(ctx.captured_queries))`
   
3. Implementasi Database Indexing
   A. Tambahkan konfigurasi indexes pada class Meta model Course di catalog/models.py:
      "indexes = [
            models.Index(fields=["is_active", "title"]),
         ]"
   
   B. Jalankan migrasi database:
      `docker compose exec app python manage.py makemigrations`
      `docker compose exec app python manage.py migrate`

   C. Uji rencana eksekusi query (EXPLAIN) di Django Shell:
      "from catalog.models import Course
       qs = Course.objects.filter(is_active=True, title="Performance Course 5000")
       print(qs.explain())"
   
4. Uji Otomatis
   Jalankan pengujian otomatis untuk memastikan seluruh fitur aplikasi tetap berfungsi tanpa merusak logic:
   `docker compose exec app python manage.py test catalog`