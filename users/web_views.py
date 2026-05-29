from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, views as auth_views, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.urls import reverse_lazy
from .forms import SignupForm, SigninForm, AccountForm
from .models import CustomUser
from team_finder.constants import PARTICIPANT_ROLES


class SignupView(generic.CreateView):
    form_class = SignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('project-list')

    def form_valid(self, f):
        r = super().form_valid(f)
        login(self.request, self.object)
        return r


class SigninView(auth_views.LoginView):
    form_class = SigninForm
    template_name = 'users/signin.html'


class SignoutView(auth_views.LogoutView):
    next_page = reverse_lazy('project-list')


class PasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('account-edit')
    success_message = 'Password changed'


class AccountDetailView(generic.DetailView):
    model = CustomUser
    template_name = 'users/user-details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kw):
        d = super().get_context_data(**kw)
        d['role_options'] = list(PARTICIPANT_ROLES.values())
        return d


class AccountEditView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    form_class = AccountForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('project-list')

    def get_object(self, qs=None):
        return self.request.user


class MemberListView(generic.ListView):
    model = CustomUser
    template_name = 'users/participants.html'
    context_object_name = 'members'
    paginate_by = 12

    def get_context_data(self, **kw):
        d = super().get_context_data(**kw)
        d['role_options'] = PARTICIPANT_ROLES
        return d

    def get_queryset(self):
        qs = super().get_queryset()
        r = self.request.GET.get('role', '')
        s = self.request.GET.get('skill', '')
        if r:
            qs = qs.filter(role=r)
        if s:
            qs = qs.filter(skills__contains=s)
        return qs.order_by('-date_joined')
