from django.contrib import admin
from .models import Project, Membership, Favorite


@admin.register(Project)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status', 'skills')
    search_fields = ('title', 'description', 'author__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'role')
    list_filter = ('role',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'created_at')
