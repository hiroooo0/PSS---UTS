# Simple LMS - Minggu 4 (Django Framework & ORM)

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