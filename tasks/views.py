import datetime

from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from tasks.forms import AddNewTaskForm, RegistrationForm
from tasks.models import Task


class TaskListView(generic.ListView, generic.FormView):
    model = Task
    form_class = AddNewTaskForm
    success_url = '/tasks/'
    initial = {'due_date': datetime.date.today()}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Task.objects.order_by('-due_date')


class TodayTasksListView(generic.ListView, generic.FormView):
    model = Task
    form_class = AddNewTaskForm
    success_url = '/tasks/today'
    initial = {'due_date': datetime.date.today()}
    template_name = 'tasks/today_task_list.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Task.objects.filter(due_date__exact=datetime.date.today())


class TaskDetailView(generic.DetailView):
    model = Task


class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('today')


class TaskUpdate(UpdateView):
    model = Task
    fields = ['task_name', 'task_description', 'due_date']


class RegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    form_class = RegistrationForm
    success_message = 'Your profile was created successfully'


# class TaskListView(generic.ListView, CreateView):
#     model = Task
#     fields = ['task_name', 'task_description', 'due_date']
#     initial = {'due_date': datetime.date.today()}


# # Create your views here.
# def index(request):
#     return render(request, 'index.html')
