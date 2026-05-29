from django.urls import path
from . import web_views

urlpatterns = [
    path('signup/', web_views.SignupView.as_view(), name='signup'),
    path('signin/', web_views.SigninView.as_view(), name='signin'),
    path('signout/', web_views.SignoutView.as_view(), name='signout'),
    path('password/', web_views.PasswordChangeView.as_view(), name='password-change'),
    path('profile/<int:pk>/', web_views.AccountDetailView.as_view(), name='profile-detail'),
    path('profile/edit/', web_views.AccountEditView.as_view(), name='account-edit'),
    path('members/', web_views.MemberListView.as_view(), name='member-list'),
]
