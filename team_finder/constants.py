"""Project-wide constants."""

from django.db import models


class ProjectState(models.TextChoices):
    """Project status options."""

    OPEN = "open", "Открыт"
    CLOSED = "closed", "Закрыт"


TITLE_MAX_LENGTH = 200
STATUS_MAX_LENGTH = 6
PHONE_MAX_LENGTH = 12
MAX_FIRST_NAME = 150
MAX_LAST_NAME = 150
ITEMS_PER_PAGE = 12
AVATAR_BG = (100, 149, 237)
AVATAR_FG = (255, 255, 255)
AVATAR_SIZE = 128

# DRF user filter constants
FILTER_FAV_AUTHORS = "fav_authors"
FILTER_MY_PARTICIPATION = "my_participation"
FILTER_LIKERS_OF_MY_PROJECTS = "likers_of_my_projects"
FILTER_PARTICIPANTS_OF_MY_PROJECTS = "participants_of_my_projects"

# HTML user filter constants
FILTER_OWNERS_OF_FAVORITE_PROJECTS = "owners-of-favorite-projects"
FILTER_OWNERS_OF_PARTICIPATING_PROJECTS = "owners-of-participating-projects"
FILTER_INTERESTED_IN_MY_PROJECTS = "interested-in-my-projects"
FILTER_PARTICIPANTS_OF_MY_PROJECTS_HTML = "participants-of-my-projects"
