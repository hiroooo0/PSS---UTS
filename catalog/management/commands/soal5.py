from django.core.management.base import BaseCommand
from django.db import connection, reset_queries
from django.test.utils import CaptureQueriesContext

from catalog.models import Course

# Jumlah Course yang diuji. Dibatasi agar log query Django (maks. 9000) tidak penuh.
N = 100


class Command(BaseCommand):
    help = "UTS Soal 5: eksperimen optimasi query"

    def handle(self, *args, **options):
        w = self.stdout.write
        w(f"Total Course di database: {Course.objects.count()}")
        w(f"Jumlah Course yang diuji : {N}")

        # a. Course + dosen TANPA select_related
        reset_queries()
        with CaptureQueriesContext(connection) as q_a:
            for c in Course.objects.all()[:N]:
                _ = c.lecturer.username
        w(f"a. Tanpa select_related    : {len(q_a)} query")

        # b. Course + dosen DENGAN select_related
        reset_queries()
        with CaptureQueriesContext(connection) as q_b:
            for c in Course.objects.select_related("lecturer")[:N]:
                _ = c.lecturer.username
        w(f"b. Dengan select_related   : {len(q_b)} query")

        # c. Course + Lesson tanpa dan dengan prefetch_related
        reset_queries()
        with CaptureQueriesContext(connection) as q_c1:
            for c in Course.objects.all()[:N]:
                _ = [l.title for l in c.lessons.all()]
        w(f"c. Tanpa prefetch_related  : {len(q_c1)} query")

        reset_queries()
        with CaptureQueriesContext(connection) as q_c2:
            for c in Course.objects.prefetch_related("lessons")[:N]:
                _ = [l.title for l in c.lessons.all()]
        w(f"c. Dengan prefetch_related : {len(q_c2)} query")

        # d. EXPLAIN
        w("d. EXPLAIN Course.objects.filter(code='PSS01'):")
        w(Course.objects.filter(code="PSS01").explain())