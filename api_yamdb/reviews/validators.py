from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

MESSAGES = getattr(settings, "MESSAGES", None)


def validator_year(year):
    if year > timezone.now().year:
        raise ValidationError(MESSAGES["no_valid_year"])
