from django.contrib import admin
from django.urls import include, path

from projects.web_views import ProjectListView

urlpatterns = [
    path('', ProjectListView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('users/', include('users.urls')),
]
