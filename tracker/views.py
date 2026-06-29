from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Issue, Project
from .forms import IssueForm, ProjectForm
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProjectUsersForm


class IssueListView(ListView):
    model = Issue
    template_name = 'issue_list.html'
    context_object_name = 'issues'

    def get_queryset(self):
        return Issue.objects.filter(
            is_deleted=False
        )
    
class IssueDetailView(DetailView):
    model = Issue
    template_name = 'issue_detail.html'
    context_object_name = 'issue'

    def get_queryset(self):
        return Issue.objects.filter(
            project__users=self.request.user,
            is_deleted=False
        )

class IssueCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issue_create.html'

    def form_valid(self, form):
        project = get_object_or_404(
            Project,
            pk=self.kwargs['pk'],
            users=self.request.user
        )

        form.instance.project = project

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'project_detail',
             kwargs={'pk': self.object.project.pk})
    
class IssueEditView(LoginRequiredMixin, UpdateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issue_edit.html'

    def get_queryset(self):
        return Issue.objects.filter(
            project__users=self.request.user,
            is_deleted=False
        )

    def get_success_url(self):
        return reverse('issue_detail', kwargs={'pk': self.object.pk})
    
class IssueDeleteView(LoginRequiredMixin, DeleteView):
    model = Issue

    def get_queryset(self):

        return Issue.objects.filter(
            project__users=self.request.user
        )

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

    def get_queryset(self):
        return Project.objects.filter(
            users=self.request.user
        )
    
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_create.html'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user

        response = super().form_valid(form)

        self.object.users.add(
            self.request.user
        )

        return response
    
    def get_success_url(self):
        return reverse_lazy(
            'project_detail',
            kwargs={
                'pk': self.object.pk
            }
        )
    
class ProjectEditView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'project_edit.html'

    def get_queryset(self):
        return Project.objects.filter(
            owner=self.request.user
        )

    def get_success_url(self):
        return reverse_lazy(
            'project_detail',
            kwargs={'pk': self.object.pk}
        )
    
class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('project_list')

    def get_queryset(self):
        return Project.objects.filter(
            owner=self.request.user
        )

class ProjectUsersView(View):
    def get(self, request, pk):
        project = get_object_or_404(
            Project,
            pk=pk,
            owner=request.user
        )

        form = ProjectUsersForm(
            initial={
                'users': project.users.all()
            }
        )

        return render(
            request,
            'project_users.html',
            {
                'project': project,
                'form': form
            }
        )


    def post(self, request, pk):
        project = get_object_or_404(
            Project,
            pk=pk,
            owner=request.user
        )

        form = ProjectUsersForm(
            request.POST
        )

        if form.is_valid():
            project.users.set(
                form.cleaned_data['users']
            )

            return redirect(
                'project_detail',
                pk=project.pk
            )

        return render(
            request,
            'project_users.html',
            {
                'project': project,
                'form': form
            }
        )