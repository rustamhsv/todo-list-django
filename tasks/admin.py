from django.contrib import admin
from tasks.models import Task, Project, Team

# Register your models here.
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Team)
