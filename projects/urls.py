from django.urls import path
from . import views


urlpatterns = [
    path('projects', views.ProjectListView.as_view(), name='projects'),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),
    path('my-projects/', views.MyProjectListView.as_view(), name='my-projects'),
]

urlpatterns += [
    path('project/create', views.ProjectCreate.as_view(), name='project-create'),
    path('project/<int:pk>/update', views.ProjectUpdate.as_view(), name='project-update'),
    path('project/<int:pk>/delete', views.ProjectDelete.as_view(), name='project-delete'),
]

