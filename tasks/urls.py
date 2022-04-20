from django.urls import path
from . import views


urlpatterns = [
    path('', views.TaskListView.as_view(), name='all-tasks'),
    path('today/', views.TodayTasksListView.as_view(), name='today'),
    path('task/<int:pk>', views.TaskDetailView.as_view(), name='task-detail')
]

urlpatterns += [
    path('task/<int:pk>/delete', views.TaskDelete.as_view(), name='task-delete'),
    path('task/<int:pk>/update', views.TaskUpdate.as_view(), name='task-update')
]

urlpatterns += [
    path('register/', views.RegistrationView.as_view(), name='register'),
]
