from django.urls import path
from .views import (
    IssueDetailView,
    IssueCreateView,
    IssueEditView,
    IssueDeleteView,
    ProjectListView,
    ProjectDetailView,
    ProjectCreateView,
    ProjectEditView,
    ProjectDeleteView
)


urlpatterns = [
    path('issue/<int:pk>/', IssueDetailView.as_view(), name='issue_detail'),
    path('issue/<int:pk>/add/', IssueCreateView.as_view(), name='issue_add'),
    path('issue/<int:pk>/edit/', IssueEditView.as_view(), name='issue_edit'),
    path('issue/<int:pk>/delete/', IssueDeleteView.as_view(), name='issue_delete'),
    path('', ProjectListView.as_view(), name='project_list'),
    path('projects/add/',ProjectCreateView.as_view(),name='project_add'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/edit/', ProjectEditView.as_view(), name='project_edit'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
]