from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import Assignment, Course, Enrollment, Lesson, Submission
from users.models import User


class Command(BaseCommand):
    help = "Membuat sample data User, Course, Lesson, Enrollment, Assignment, Submission (idempotent)"

    def _get_user(self, username, email, role, password="12345"):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "role": role},
        )
        if created:
            user.set_password(password)
            user.save()
        return user

    def handle(self, *args, **options):

        lecturer = self._get_user("suprayogi", "suprayogi@gmail.com", User.Role.LECTURER)
        student = self._get_user("fauzan", "fauzan@gmail.com", User.Role.STUDENT)
        for nama in ["agus", "ayu", "bagus", "heru"]:
            self._get_user(nama, f"{nama}@gmail.com", User.Role.LECTURER, password="123")

        courses = [
            ("PSS01", "Pemrograman Sisi Server", "Belajar backend development dengan Django."),
            ("PSS02", "Django Framework", "Mempelajari framework Django dan struktur project."),
            ("PSS03", "Django ORM", "Mempelajari database dan ORM menggunakan Django."),
            ("PSS04", "REST API", "Mempelajari pembuatan REST API dengan Django."),
            ("PSS05", "Docker", "Mempelajari containerisasi aplikasi Django."),
        ]
        for code, title, description in courses:
            Course.objects.get_or_create(
                code=code,
                defaults={"title": title, "description": description, "lecturer": lecturer},
            )
        course = Course.objects.get(code="PSS01")

        lessons = [
            "Pengenalan Backend",
            "Pola Arsitektur Backend",
            "Kontainerisasi dengan Docker",
        ]
        for order, title in enumerate(lessons, start=1):
            Lesson.objects.get_or_create(
                course=course, order=order, defaults={"title": title}
            )

        Enrollment.objects.get_or_create(student=student, course=course)

        assignment1, _ = Assignment.objects.get_or_create(
            course=course,
            title="Tugas Django ORM",
            defaults={
                "description": "Implementasikan model dan relationship menggunakan Django ORM.",
                "deadline": timezone.now() + timedelta(days=7),
            },
        )
        assignment2, _ = Assignment.objects.get_or_create(
            course=course,
            title="Tugas REST API",
            defaults={
                "description": "Buat REST API sederhana menggunakan Django.",
                "deadline": timezone.now() + timedelta(days=14),
            },
        )

        Submission.objects.get_or_create(
            assignment=assignment1,
            student=student,
            defaults={
                "content": "Saya telah menyelesaikan implementasi Django ORM.",
                "grade": Decimal("87.50"),
            },
        )
        Submission.objects.get_or_create(
            assignment=assignment2,
            student=student,
            defaults={
                "content": "Saya telah menyelesaikan REST API menggunakan Django.",
                "grade": Decimal("90.00"),
            },
        )

        self.stdout.write(self.style.SUCCESS("Sample data berhasil dibuat."))
        self.stdout.write(
            f"User={User.objects.count()} Course={Course.objects.count()} "
            f"Lesson={Lesson.objects.count()} Enrollment={Enrollment.objects.count()} "
            f"Assignment={Assignment.objects.count()} Submission={Submission.objects.count()}"
        )