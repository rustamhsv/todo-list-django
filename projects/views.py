from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from tasks.models import Project


class ProjectListView(generic.ListView):
    model = Project


class MyProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    redirect_field_name = 'login'

    def get_queryset(self):
        return Project.objects.filter(user__exact=self.request.user)


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    redirect_field_name = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get the project by primary key
        projects = Project.objects.filter(pk=self.kwargs['pk'])

        users = None
        if projects:
            users = projects[0].user.all()

        context['users'] = users
        return context


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['title', 'description', 'user']
    redirect_field_name = 'login'


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['title', 'description', 'user']
    template_name = 'tasks/project_update_form.html'
    redirect_field_name = 'login'


class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('projects')
    redirect_field_name = 'login'
