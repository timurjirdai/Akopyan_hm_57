from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Issue, Project
from .forms import IssueForm, ProjectForm
from django.db.models import Q
from django.urls import reverse_lazy, reverse


class IssueListView(ListView):
    template_name = 'issue_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = Issue.objects.filter(is_deleted=False)
        return context
    
class IssueDetailView(DetailView):
    model = Issue
    template_name = 'issue_detail.html'
    context_object_name = 'issue'

class IssueCreateView(CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issue_create.html'

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        form.instance.project = project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.pk})
    
class IssueEditView(UpdateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issue_edit.html'

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.pk})
    
class IssueDeleteView(DeleteView):
    model = Issue

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.pk})

class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'
    paginate_by = 5

    def get_queryset(self):
        projects = Project.objects.all()
        search = self.request.GET.get('search')

        if search:
            projects = projects.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        return projects
    
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'
    
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_create.html'
    success_url = reverse_lazy('project_list')
    
class ProjectEditView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_edit.html'

    def get_success_url(self):
        return reverse_lazy(
            'project_detail',
            kwargs={'pk': self.object.pk}
        )
    
class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('project_list')