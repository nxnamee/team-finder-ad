from django.contrib.auth import views as auth_views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from team_finder.constants import ITEMS_PER_PAGE
from users.forms import EmailAuthenticationForm, ProfileEditForm, UserRegistrationForm

User = get_user_model()


class RegisterView(CreateView):

    form_class = UserRegistrationForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse('users:login')


class EmailLoginView(auth_views.LoginView):

    authentication_form = EmailAuthenticationForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return self.get_redirect_url() or reverse('projects:project-list')


class UserDetailView(DetailView):

    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'


class EditProfileView(LoginRequiredMixin, UpdateView):

    model = User
    form_class = ProfileEditForm
    template_name = 'users/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['user'] = self.request.user
        return context_data

    def get_success_url(self):
        return reverse('users:user-detail', kwargs={'pk': self.request.user.pk})


class UserListView(ListView):

    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        base_queryset = User.objects.all().order_by('-date_joined')
        if not self.request.user.is_authenticated:
            return base_queryset

        active_filter_param = self.request.GET.get('filter')
        if active_filter_param == 'owners-of-favorite-projects':
            return base_queryset.filter(projects__favorited_by=self.request.user).distinct()
        if active_filter_param == 'owners-of-participating-projects':
            return base_queryset.filter(projects__participants=self.request.user).distinct()
        if active_filter_param == 'interested-in-my-projects':
            return base_queryset.filter(favorite_projects__author=self.request.user).distinct()
        if active_filter_param == 'participants-of-my-projects':
            return base_queryset.filter(joined_projects__author=self.request.user).distinct()
        return base_queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['active_filter'] = self.request.GET.get('filter')
        return context_data


class UserPasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):

    template_name = 'users/change_password.html'
    success_url = None

    def get_success_url(self):
        return reverse('users:user-detail', kwargs={'pk': self.request.user.pk})
