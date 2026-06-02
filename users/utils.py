"""Utility functions for the users app."""

import io

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from team_finder.constants import AVATAR_BG, AVATAR_FG, AVATAR_SIZE


def _build_avatar(letter):
    """Generate a solid-colour avatar with the given letter."""
    img = Image.new("RGB", (AVATAR_SIZE, AVATAR_SIZE), AVATAR_BG)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), letter, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (AVATAR_SIZE - tw) // 2
    y = (AVATAR_SIZE - th) // 2 - 5
    draw.text((x, y), letter, fill=AVATAR_FG, font=font)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return ContentFile(buf.getvalue())
