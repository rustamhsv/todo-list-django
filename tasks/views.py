import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from tasks.forms import AddNewTaskForm
from tasks.models import Task


class TaskListView(generic.ListView, generic.FormView):
    model = Task
    form_class = AddNewTaskForm
    success_url = '/tasks/'
    initial = {'due_date': datetime.date.today()}

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class TaskDetailView(generic.DetailView):
    model = Task


class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('today')


class TaskUpdate(UpdateView):
    model = Task
    fields = ['task_name', 'task_description', 'due_date']

# class TaskListView(generic.ListView, CreateView):
#     model = Task
#     fields = ['task_name', 'task_description', 'due_date']
#     initial = {'due_date': datetime.date.today()}


# # Create your views here.
# def index(request):
#     return render(request, 'index.html')
