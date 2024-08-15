from django.utils import timezone
from django.utils.translation import gettext_lazy
from rest_framework import serializers

MESSAGE_COREAPI_MUST_BE_INSTALLED = gettext_lazy(
    "coreapi must be installed to use `get_schema_fields()`"
)


MESSAGE_UNKNOWN_OBJECT_TYPE = "Unknown object type"

EXCEPTION_NON_EXIST_DATA_TABLE = serializers.ValidationError(
    gettext_lazy("Non existing data table for this project. Please create one")
)


TEMPORARY_FILES_EXPIRATION_TIME_DELTA = timezone.timedelta(days=7)
