from django.core.management.base import BaseCommand
from django.db import connection, reset_queries

from catalog.models import Course


class Command(BaseCommand):
    help = "Membandingkan jumlah query dengan dan tanpa select_related/prefetch_related"

    def handle(self, *args, **options):
        # 1. Tanpa select_related
        reset_queries()
        for course in Course.objects.all():
            course.lecturer.username
        self.stdout.write(f"Tanpa select_related   : {len(connection.queries)} query")

        # 2. Dengan select_related
        reset_queries()
        for course in Course.objects.select_related("lecturer"):
            course.lecturer.username
        self.stdout.write(f"Dengan select_related  : {len(connection.queries)} query")

        # 3. Tanpa prefetch_related
        reset_queries()
        for course in Course.objects.all():
            list(course.lessons.all())
        self.stdout.write(f"Tanpa prefetch_related : {len(connection.queries)} query")

        # 4. Dengan prefetch_related
        reset_queries()
        for course in Course.objects.prefetch_related("lessons"):
            list(course.lessons.all())
        self.stdout.write(f"Dengan prefetch_related: {len(connection.queries)} query")