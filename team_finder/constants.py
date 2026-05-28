from django.db import models


class ProjectState(models.TextChoices):
    OPEN = 'open', 'Открыт'
    CLOSED = 'closed', 'Закрыт'


TITLE_MAX_LENGTH = 200
STATUS_MAX_LENGTH = 6
PHONE_MAX_LENGTH = 12
NAME_MAX_LENGTH = 150
SURNAME_MAX_LENGTH = 150
ITEMS_PER_PAGE = 12
AVATAR_BACKGROUND_COLOR = (100, 149, 237)
AVATAR_TEXT_COLOR = (255, 255, 255)
AVATAR_SIZE = 128
