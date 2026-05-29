from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'projects', views.ListingViewSet, basename='api-project')

urlpatterns = [
    path('', include(router.urls)),
]
