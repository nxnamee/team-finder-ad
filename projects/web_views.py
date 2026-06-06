"""HTML views for the projects app."""

from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from projects.forms import ProjectForm
from projects.models import Project
from team_finder.constants import ITEMS_PER_PAGE, ProjectState


class ProjectListView(ListView):
    """Paginated project listing with favorite state."""

    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        """Eager-load author and participants."""
        return Project.objects.select_related("author").prefetch_related("participants")

    def get_context_data(self, **kwargs):
        """Inject set of favorited project IDs for the current user."""
        ctx = super().get_context_data(**kwargs)
        ctx["favorite_project_ids"] = set()
        if self.request.user.is_authenticated:
            ctx["favorite_project_ids"] = set(
                self.request.user.favorite_projects.values_list("id", flat=True)
            )
        return ctx


class FavoriteProjectsView(LoginRequiredMixin, ListView):
    """Shows projects the current user has favorited."""

    template_name = "projects/favorite_projects.html"
    context_object_name = "projects"
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        """Favorited projects for the current user."""
        return (
            self.request.user.favorite_projects.select_related("author")
            .prefetch_related("participants")
            .distinct()
        )

    def get_context_data(self, **kwargs):
        """Inject set of favorited project IDs."""
        ctx = super().get_context_data(**kwargs)
        ctx["favorite_project_ids"] = set(
            self.request.user.favorite_projects.values_list("id", flat=True)
        )
        return ctx


class ProjectDetailView(DetailView):
    """Single project detail view."""

    model = Project
    template_name = "projects/project-details.html"


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Create a new project."""

    model = Project
    form_class = ProjectForm
    template_name = "projects/create-project.html"

    def get_context_data(self, **kwargs):
        """Signal that this is a create action."""
        ctx = super().get_context_data(**kwargs)
        ctx["is_edit"] = False
        return ctx

    def form_valid(self, form):
        """Assign the current user as author."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit an existing project (author only)."""

    model = Project
    form_class = ProjectForm
    template_name = "projects/create-project.html"

    def test_func(self):
        """Only the author may edit."""
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        """Signal that this is an edit action."""
        ctx = super().get_context_data(**kwargs)
        ctx["is_edit"] = True
        return ctx


@login_required
@require_POST
def toggle_favorite(request, pk):
    """Toggle a project's favorite status for the current user."""
    obj = get_object_or_404(Project, pk=pk)
    usr = request.user
    if usr.favorite_projects.filter(pk=obj.pk).exists():
        obj.favorited_by.remove(usr)
        return JsonResponse({"status": "ok", "favorite": False})

    obj.favorited_by.add(usr)
    return JsonResponse({"status": "ok", "favorite": True})


@login_required
@require_POST
def toggle_participate(request, pk):
    """Join or leave a project."""
    obj = get_object_or_404(Project, pk=pk)
    if obj.author == request.user:
        return JsonResponse(
            {"status": "error", "message": "Cannot join your own project"},
            status=HTTPStatus.BAD_REQUEST,
        )
    if obj.status != ProjectState.OPEN:
        return JsonResponse(
            {"status": "error", "message": "Project is closed"},
            status=HTTPStatus.BAD_REQUEST,
        )

    joined = obj.participants.filter(pk=request.user.pk).exists()
    if joined:
        obj.participants.remove(request.user)
    else:
        obj.participants.add(request.user)
    return JsonResponse({"status": "ok", "participant": not joined})


@login_required
@require_POST
def complete_project(request, pk):
    """Mark a project as closed."""
    obj = get_object_or_404(Project, pk=pk)
    if obj.author != request.user:
        return JsonResponse(
            {"status": "error", "message": "Not the author"},
            status=HTTPStatus.FORBIDDEN,
        )
    obj.status = ProjectState.CLOSED
    obj.save(update_fields=["status"])
    return JsonResponse({"status": "ok"})
