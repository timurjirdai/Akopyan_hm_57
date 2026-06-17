from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from .models import Issue, Project
from .forms import IssueForm, ProjectForm

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

class IssueCreateView(TemplateView):
    def get(self, request):
        form = IssueForm()
        return render(request, 'issue_create.html', {'form': form})
    
    def post(self, request):
        form = IssueForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('issue_list')
        
        return render(request, 'issue_create.html', {'form': form})
    
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
        issue.delete()
        return redirect('issue_list')
    
class ProjectListView(TemplateView):
    template_name = 'project_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context
    
class ProjectDetailView(TemplateView):
    template_name = 'project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(
            Project,
            pk=self.kwargs['pk']
        )
        return context
    
class ProjectCreateView(View):
    def get(self, request):
        form = ProjectForm()

        return render(
            request,
            'project_create.html',
            {'form': form}
        )

    def post(self, request):
        form = ProjectForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('project_list')

        return render(
            request,
            'project_create.html',
            {'form': form}
        )
    
class ProjectEditView(View):
    def get(self, request, pk):
        project = get_object_or_404(
            Project,
            pk=pk
        )

        form = ProjectForm(instance=project)

        return render(
            request,
            'project_edit.html',
            {
                'form': form,
                'project': project
            }
        )

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            return redirect(
                'project_detail',
                pk=project.pk
            )

        return render(
            request,
            'project_edit.html',
            {
                'form': form,
                'project': project
            }
        )
    
class ProjectDeleteView(View):
    def post(self, request, pk):
        project = get_object_or_404(
            Project,
            pk=pk
        )
        project.delete()
        
        return redirect('project_list')