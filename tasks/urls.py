from django.urls import path
from . import views


urlpatterns = [
    path('', views.TaskListView.as_view(), name='all-tasks'),
    path('today/', views.TodayTasksListView.as_view(), name='today'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),
    path('my-tasks/', views.MyTasksListView.as_view(), name='my-tasks'),
    # path('projects', views.ProjectListView.as_view(), name='projects'),
    # path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),
    # path('my-projects/', views.MyProjectListView.as_view(), name='my-projects'),
]

urlpatterns += [
    path('task/<int:pk>/delete', views.TaskDelete.as_view(), name='task-delete'),
    path('task/<int:pk>/update', views.TaskUpdate.as_view(), name='task-update'),
    # path('project/create', views.ProjectCreate.as_view(), name='project-create'),
    # path('project/<int:pk>/update', views.ProjectUpdate.as_view(), name='project-update'),
    # path('project/<int:pk>/delete', views.ProjectDelete.as_view(), name='project-delete'),
]

urlpatterns += [
    path('register/', views.RegistrationView.as_view(), name='register'),
]
