from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def valid_url(value):
    url_validator = URLValidator()
    try:
        url_validator(value)
    except Exception:
        raise ValidationError("Invalid URL")
    return value
