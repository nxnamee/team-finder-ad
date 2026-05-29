from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                ("status", models.CharField(choices=[("open", "Открыт"), ("closed", "Закрыт")], default="open", max_length=6, verbose_name="Статус")),
                ("pub_date", models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="projects", to=settings.AUTH_USER_MODEL, verbose_name="Автор")),
                ("participants", models.ManyToManyField(blank=True, related_name="joined_projects", to=settings.AUTH_USER_MODEL, verbose_name="Участники")),
                ("favorited_by", models.ManyToManyField(blank=True, related_name="favorite_projects", to=settings.AUTH_USER_MODEL, verbose_name="Добавили в избранное")),
            ],
            options={
                "verbose_name": "Проект",
                "verbose_name_plural": "Проекты",
                "ordering": ("-pub_date",),
            },
        ),
    ]
