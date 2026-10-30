from django.core.management.base import BaseCommand

from catalog.models import Assignment, Course, Enrollment, Lesson, Submission
from users.models import User


class Command(BaseCommand):
    help = "UTS Soal 4b: query ORM"

    def handle(self, *args, **options):
        w = self.stdout.write

        w("\n1. Semua Course beserta kode dan judulnya")
        w(str(list(Course.objects.values_list("code", "title"))))

        dosen = User.objects.get(username="suprayogi")
        w(f"\n2. Course yang diampu {dosen.username}")
        w(str(list(Course.objects.filter(lecturer=dosen).values_list("code", "title"))))

        course = Course.objects.get(code="PSS01")
        w(f"\n3. Lesson milik {course.code}")
        w(str(list(Lesson.objects.filter(course=course).order_by("order").values_list("order", "title"))))

        w(f"\n4. Jumlah mahasiswa terdaftar pada {course.code}")
        w(str(Enrollment.objects.filter(course=course).count()))

        w(f"\n5. Assignment milik {course.code}")
        w(str(list(Assignment.objects.filter(course=course).values_list("title", "deadline"))))

        assignment = Assignment.objects.get(title="Tugas Django ORM")
        w(f"\n6. Submission milik assignment '{assignment.title}'")
        w(str(list(Submission.objects.filter(assignment=assignment).values_list("student__username", "grade"))))