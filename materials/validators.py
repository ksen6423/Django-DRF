from urllib.parse import urlparse

from rest_framework.exceptions import ValidationError


ALLOWED_YOUTUBE_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
}


def validate_no_external_links(value: str) -> str:
    hostname = (urlparse(value).hostname or "").lower()
    if hostname not in ALLOWED_YOUTUBE_HOSTS:
        raise ValidationError(
            "Разрешены только ссылки на домен youtube.com."
        )
    return value
