"""HTML views for the users app."""

from django.contrib.auth import login as auth_login, views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from team_finder.constants import (
    FILTER_INTERESTED_IN_MY_PROJECTS,
    FILTER_OWNERS_OF_FAVORITE_PROJECTS,
    FILTER_OWNERS_OF_PARTICIPATING_PROJECTS,
    FILTER_PARTICIPANTS_OF_MY_PROJECTS_HTML,
    ITEMS_PER_PAGE,
)
from users.forms import EmailAuthenticationForm, ProfileEditForm, UserRegistrationForm

User = get_user_model()


class RegisterView(CreateView):
    """User registration view."""

    form_class = UserRegistrationForm
    template_name = "users/register.html"

    def form_valid(self, form):
        """Auto-login after successful registration."""
        resp = super().form_valid(form)
        auth_login(self.request, self.object)
        return resp

    def get_success_url(self):
        """Redirect to project list after registration."""
        return reverse("projects:project-list")


class EmailLoginView(auth_views.LoginView):
    """Login by email address."""

    authentication_form = EmailAuthenticationForm
    template_name = "users/login.html"

    def get_success_url(self):
        """Redirect to project list by default."""
        return self.get_redirect_url() or reverse("projects:project-list")


class UserDetailView(DetailView):
    """Public profile page."""

    model = User
    template_name = "users/user-details.html"
    context_object_name = "user"


class EditProfileView(LoginRequiredMixin, UpdateView):
    """Profile editor for the current user."""

    model = User
    form_class = ProfileEditForm
    template_name = "users/edit_profile.html"

    def get_object(self, queryset=None):
        """Always edit the current user."""
        return self.request.user

    def get_context_data(self, **kwargs):
        """Expose current user in template context."""
        ctx = super().get_context_data(**kwargs)
        ctx["user"] = self.request.user
        return ctx

    def get_success_url(self):
        """Back to profile after save."""
        return reverse("users:user-detail", kwargs={"pk": self.request.user.pk})


class UserListView(ListView):
    """Paginated user directory with optional filter chips."""

    model = User
    template_name = "users/participants.html"
    context_object_name = "participants"
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        """Apply active filter if present."""
        qs = User.objects.all()
        if not self.request.user.is_authenticated:
            return qs

        fltr = self.request.GET.get("filter")
        if fltr == FILTER_OWNERS_OF_FAVORITE_PROJECTS:
            return qs.filter(projects__favorited_by=self.request.user).distinct()
        if fltr == FILTER_OWNERS_OF_PARTICIPATING_PROJECTS:
            return qs.filter(projects__participants=self.request.user).distinct()
        if fltr == FILTER_INTERESTED_IN_MY_PROJECTS:
            return qs.filter(favorite_projects__author=self.request.user).distinct()
        if fltr == FILTER_PARTICIPANTS_OF_MY_PROJECTS_HTML:
            return qs.filter(joined_projects__author=self.request.user).distinct()
        return qs

    def get_context_data(self, **kwargs):
        """Pass current filter to the template."""
        ctx = super().get_context_data(**kwargs)
        ctx["active_filter"] = self.request.GET.get("filter")
        return ctx


class UserPasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    """Password change form."""

    template_name = "users/change_password.html"

    def get_success_url(self):
        """Redirect to profile after change."""
        return reverse("users:user-detail", kwargs={"pk": self.request.user.pk})
