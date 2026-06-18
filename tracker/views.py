from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Issue, Project
from .forms import IssueForm, ProjectForm
from django.db.models import Q
from django.urls import reverse_lazy


class IssueListView(TemplateView):
    template_name = 'issue_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issues'] = Issue.objects.all()
        return context
    
class IssueDetailView(TemplateView):
    template_name = 'issue_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = get_object_or_404(
            Issue.objects.prefetch_related('types'),
            id=self.kwargs['pk'])

        return context

class IssueCreateView(View):
    def get(self, request, pk):
        form = IssueForm()

        return render(
            request,
            'issue_create.html',
            {'form': form}
        )

    def post(self, request, pk):
        project = get_object_or_404(
            Project,
            pk=pk
        )

        form = IssueForm(request.POST)

        if form.is_valid():
            issue = form.save(commit=False)
            issue.project = project
            issue.save()
            form.save_m2m()

            return redirect(
                'project_detail',
                pk=project.pk
            )

        return render(
            request,
            'issue_create.html',
            {'form': form}
        )
    
class IssueEditView(TemplateView):
    def get(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        form = IssueForm(instance=issue)

        return render(request, 'issue_edit.html', 
                {'form': form, 
                'issue': issue})
    
    def post(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        form = IssueForm(request.POST, instance=issue)
        
        if form.is_valid():
            form.save()
            return redirect('issue_detail', pk=issue.pk)
        
        return render(request, 'issue_edit.html', 
                      {'form': form,
                       'issue': issue})
    
class IssueDeleteView(View):
    def post(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        project_pk = issue.project.pk
        issue.delete()
        return redirect('project_detail', pk=project_pk)
    
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