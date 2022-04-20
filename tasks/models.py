import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.urls import reverse


class Project(models.Model):
    """ Model for projects """
    title = models.CharField(max_length=100, help_text='Enter project title')
    user = models.ManyToManyField(User, help_text='Assign user to this project', blank=True)

    """ String representation for Projects model """
    def __str__(self):
        return self.title


class Task(models.Model):
    """ Model for tasks """
    task_name = models.CharField(max_length=100, help_text='Enter task name')
    task_description = models.CharField(max_length=200, help_text='Enter task description',
                                        blank=True)
    due_date = models.DateField()
    files = models.FileField(upload_to='attachments/%Y/%m/%d', blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ManyToManyField(User, help_text='Assign user to this task', blank=True)

    @property
    def is_expired(self):
        if self.due_date < datetime.date.today():
            return True
        return False

    def __str__(self):
        """ String representation for model object """
        return self.task_name

    def get_absolute_url(self):
        return reverse('task-detail', args=[str(self.id)])


# class Team(models.Model):
#     name = models.CharField(max_length=100, help_text='Enter name for team member')
#     email = models.EmailField(max_length=100, help_text='Enter email for team member')
#     phone = models.CharField(max_length=100, help_text='Enter phone number for team member', blank=True)
#     profile_pic = models.ImageField(upload_to='profile_pics/%Y/%m/%d', help_text='Upload profile picture',
#                                     blank=True, null=True)
#     # task = models.ManyToManyField(Task, help_text='Assign task for team member', blank=True)
#     # project = models.ManyToManyField(Project, help_text='Assign project for team member', blank=True)
#
#     def __str__(self):
#         """String for representing the Model object."""
#         return self.name
