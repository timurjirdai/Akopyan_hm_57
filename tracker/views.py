from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, View
from .models import Issue
from .forms import IssueForm

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
            Issue,
            id=self.kwargs['pk']
        )

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