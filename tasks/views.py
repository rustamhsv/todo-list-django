import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from tasks.forms import AddNewTaskForm, RegistrationForm, AddMyTaskForm, EmailForm
from tasks.models import Task, Project
from tasks.tasks import get_google_calendar_events


class TaskListView(LoginRequiredMixin, generic.ListView, generic.FormView):
    model = Task
    form_class = AddNewTaskForm
    success_url = '/tasks/'
    initial = {'due_date': datetime.date.today()}
    redirect_field_name = 'login'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Task.objects.order_by('-due_date')


class TodayTasksListView(LoginRequiredMixin, generic.ListView, generic.FormView):
    model = Task
    form_class = AddNewTaskForm
    success_url = '/tasks/today'
    initial = {'due_date': datetime.date.today()}
    template_name = 'tasks/today_task_list.html'
    redirect_field_name = 'login'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Task.objects.filter(due_date__exact=datetime.date.today())


class MyTasksListView(LoginRequiredMixin, generic.ListView, generic.FormView):
    model = Task
    form_class = AddMyTaskForm
    success_url = '/tasks/my-tasks'
    initial = {'due_date': datetime.date.today()}
    template_name = 'tasks/my_task_list.html'
    redirect_field_name = 'login'

    def form_valid(self, form):
        # manually save data to db & assign task for logged in user
        my_task = Task.objects.create(
            task_name=form.cleaned_data['task_name'],
            task_description=form.cleaned_data['task_description'],
            due_date=form.cleaned_data['due_date'],
            files=form.cleaned_data['files'],
            project=form.cleaned_data['project'],
        )

        # cannot set ManyToManyField in create methods, have to add later on
        my_task.user.add(self.request.user)

        # save to db
        my_task.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Task.objects.filter(user__exact=self.request.user)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    redirect_field_name = 'login'
    
    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data()
        
        # get task by primary key
        tasks = Task.objects.filter(pk=self.kwargs['pk'])
        
        # get users
        users = None
        if tasks:
            users = tasks[0].user.all()
            print('FILES: ', tasks[0].files)
        
        context['users'] = users
        return context
        

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('today')
    redirect_field_name = 'login'


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['task_name', 'task_description', 'due_date', 'files', 'user', 'project']
    redirect_field_name = 'login'


class RegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    form_class = RegistrationForm
    success_message = 'Your profile was created successfully'


def integrate_google_calender(request):
    get_google_calendar_events(request.user)
    return HttpResponseRedirect('/tasks/calendar-integrated/')

    # if request.method == 'POST':
    #     form = EmailForm(request.POST)
    #
    #     if form.is_valid():
    #         get_google_calendar_events(request.user)
    #         return HttpResponseRedirect('/tasks/calendar-integrated/')
    #
    # else:
    #     form = EmailForm()
    #     context = {'form': form}
    #     return render(request, 'google_calendar.html', context=context)


def calendar_integrated(request):
    return render(request, 'calendar_integrated.html')

# class TaskListView(generic.ListView, CreateView):
#     model = Task
#     fields = ['task_name', 'task_description', 'due_date']
#     initial = {'due_date': datetime.date.today()}


# # Create your views here.
# def index(request):
#     return render(request, 'index.html')
