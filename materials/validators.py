import re
from rest_framework.exceptions import ValidationError


def validate_no_external_links(value):
    url_pattern = re.compile(r'https?://[^\s]+|www\.[^\s]+')
    urls = url_pattern.findall(value)

    for url in urls:
        clean_url = url.lower().replace('www.', '')
        if 'youtube.com' not in clean_url:
            raise ValidationError(
                f"Ссылка '{url}' запрещена. Разрешены только ссылки на youtube.com."
            )

    return value
