from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import generic
from django.urls import reverse_lazy
from .models import Project, Membership, Favorite
from .forms import ListingForm
from team_finder.constants import PROJECT_STATUSES, PROJECT_FILTERS, PARTICIPANT_ROLES


class CatalogueView(generic.ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):
        q = self.request.GET.get('filter', 'all')
        u = self.request.user
        qs = Project.objects.all()

        if q == 'my_projects' and u.is_authenticated:
            qs = qs.filter(author=u)
        elif q == 'participating' and u.is_authenticated:
            qs = qs.filter(memberships__user=u)
        elif q == 'favorites' and u.is_authenticated:
            qs = qs.filter(favorited_by__user=u)

        return qs.select_related('author').prefetch_related('memberships').distinct()

    def get_context_data(self, **kw):
        d = super().get_context_data(**kw)
        d['filter_options'] = PROJECT_STATUSES
        d['current_filter'] = self.request.GET.get('filter', 'all')
        d['filters_map'] = PROJECT_FILTERS
        return d


class SavedProjectsView(LoginRequiredMixin, generic.ListView):
    model = Favorite
    template_name = 'projects/favorite_projects.html'
    context_object_name = 'saved_items'
    paginate_by = 12

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('project__author')


class ListingDetailView(generic.DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'

    def get_context_data(self, **kw):
        d = super().get_context_data(**kw)
        p = self.object
        u = self.request.user
        d['is_author'] = u.is_authenticated and p.author == u
        d['is_participant'] = u.is_authenticated and p.memberships.filter(user=u).exists()
        d['is_favorite'] = u.is_authenticated and p.favorited_by.filter(user=u).exists()
        d['role_options'] = list(PARTICIPANT_ROLES.values())
        d['statuses'] = PROJECT_STATUSES
        return d


class ListingCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ListingForm
    template_name = 'projects/create-project.html'
    success_url = reverse_lazy('project-list')

    def form_valid(self, f):
        f.instance.author = self.request.user
        return super().form_valid(f)


class ListingUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    form_class = ListingForm
    template_name = 'projects/edit.html'
    success_url = reverse_lazy('project-list')

    def get_queryset(self):
        return Project.objects.filter(author=self.request.user)


def toggle_saved(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'login required'}, status=401)
    p = get_object_or_404(Project, pk=pk)
    f, created = Favorite.objects.get_or_create(user=request.user, project=p)
    if not created:
        f.delete()
        return JsonResponse({'saved': False})
    return JsonResponse({'saved': True})


def toggle_teammate(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'login required'}, status=401)
    p = get_object_or_404(Project, pk=pk)
    if p.status != 'active':
        return JsonResponse({'error': 'project closed'}, status=400)
    m, created = Membership.objects.get_or_create(project=p, user=request.user, defaults={'role': 'developer'})
    if not created:
        m.delete()
        return JsonResponse({'joined': False})
    return JsonResponse({'joined': True})


def close_listing(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'login required'}, status=401)
    p = get_object_or_404(Project, pk=pk)
    if p.author != request.user:
        return JsonResponse({'error': 'not owner'}, status=403)
    p.status = 'closed'
    p.save()
    return JsonResponse({'status': 'closed'})
