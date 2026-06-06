"""Admin configuration for projects."""

from django.contrib import admin

from projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Project admin with list/search/filter and inline status editing."""

    list_display = ("title", "author", "status", "participant_count", "pub_date")
    list_editable = ("status",)
    search_fields = ("title", "description", "author__username")
    list_filter = ("status", "pub_date")
    readonly_fields = ("pub_date", "updated_at")

    @admin.display(description="Участники")
    def participant_count(self, obj):
        """Display number of participants."""
        return obj.participants.count()
