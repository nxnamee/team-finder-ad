from django.urls import path
from . import web_views

urlpatterns = [
    path('', web_views.CatalogueView.as_view(), name='project-list'),
    path('saved/', web_views.SavedProjectsView.as_view(), name='saved-projects'),
    path('project/<int:pk>/', web_views.ListingDetailView.as_view(), name='project-detail'),
    path('project/create/', web_views.ListingCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/edit/', web_views.ListingUpdateView.as_view(), name='project-edit'),
    path('api/toggle-saved/<int:pk>/', web_views.toggle_saved, name='toggle-saved'),
    path('api/toggle-join/<int:pk>/', web_views.toggle_teammate, name='toggle-join'),
    path('api/close/<int:pk>/', web_views.close_listing, name='close-listing'),
]
