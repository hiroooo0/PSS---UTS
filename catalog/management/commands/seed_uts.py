from django.core.management.base import BaseCommand

from catalog.models import Assignment, Course, Enrollment, Lesson, Submission
from users.models import User


class Command(BaseCommand):
    help = "Melengkapi data minimal UTS (idempotent)"

    def handle(self, *args, **options):
        budi, created = User.objects.get_or_create(
            username="budi",
            defaults={"email": "budi@gmail.com", "role": User.Role.STUDENT},
        )
        if created:
            budi.set_password("12345")
            budi.save()

        fauzan = User.objects.get(username="fauzan")
        pss01 = Course.objects.get(code="PSS01")
        Enrollment.objects.get_or_create(student=fauzan, course=pss01)
        Enrollment.objects.get_or_create(student=budi, course=pss01)

        self.stdout.write(
            f"Dosen={User.objects.filter(role='LECTURER').count()} "
            f"Mahasiswa={User.objects.filter(role='STUDENT').count()} "
            f"Course={Course.objects.count()} "
            f"Lesson(PSS01)={Lesson.objects.filter(course=pss01).count()} "
            f"Enrollment={Enrollment.objects.count()} "
            f"Assignment={Assignment.objects.count()} "
            f"Submission={Submission.objects.count()}"
        )
