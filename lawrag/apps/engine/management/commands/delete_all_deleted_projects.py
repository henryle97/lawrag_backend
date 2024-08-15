from django.core.management.base import BaseCommand

from lawrag.apps.engine import models


class Command(BaseCommand):
    help = "Permanently delete all deleted projects"

    def handle(self, *args, **kwargs):
        yn = input("Delete all deleted project? (y/n): ")
        if yn not in ["y", "n"]:
            print('Only type "y" or "n"')
            exit(1)
        if yn == "n":
            exit(0)
        deleted_projects = models.Project.objects.filter(deleted=True)
        num_deleted = 0
        for project in deleted_projects:
            project_name = project.name
            project.delete()
            print(f"Deleted project: {project_name}")
            num_deleted += 1
        print(f"Deleted {num_deleted} projects.")
