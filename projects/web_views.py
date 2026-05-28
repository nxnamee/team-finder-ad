from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from projects.forms import ProjectForm
from projects.models import Project
from team_finder.constants import ITEMS_PER_PAGE, ProjectState


class ProjectListView(ListView):

    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        return Project.objects.select_related('author').prefetch_related('participants')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['favorite_project_ids'] = set()
        if self.request.user.is_authenticated:
            context_data['favorite_project_ids'] = set(
                self.request.user.favorite_projects.values_list('id', flat=True)
            )
        return context_data


class FavoriteProjectsView(LoginRequiredMixin, ListView):

    template_name = 'projects/favorite_projects.html'
    context_object_name = 'projects'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        return self.request.user.favorite_projects.select_related('author').distinct()

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['favorite_project_ids'] = set(
            self.request.user.favorite_projects.values_list('id', flat=True)
        )
        return context_data


class ProjectDetailView(DetailView):

    model = Project
    template_name = 'projects/project-details.html'


class ProjectCreateView(LoginRequiredMixin, CreateView):

    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['is_edit'] = False
        return context_data

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['is_edit'] = True
        return context_data


@login_required
@require_POST
def toggle_favorite(request, pk):
    project = get_object_or_404(Project, pk=pk)
    current_user = request.user
    if current_user.favorite_projects.filter(pk=project.pk).exists():
        project.favorited_by.remove(current_user)
        return JsonResponse({'status': 'ok', 'favorite': False})
    else:
        project.favorited_by.add(current_user)
        return JsonResponse({'status': 'ok', 'favorite': True})


@login_required
@require_POST
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.author == request.user:
        return JsonResponse({'status': 'error'}, status=HTTPStatus.BAD_REQUEST)

    is_participant = project.participants.filter(pk=request.user.pk).exists()
    if is_participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return JsonResponse({'status': 'ok', 'participant': not is_participant})


@login_required
@require_POST
def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, author=request.user)
    project.status = ProjectState.CLOSED
    project.save(update_fields=['status'])
    return JsonResponse({'status': 'ok'})
