from django.apps import apps
from django.urls import include, path

urlpatterns = [
    path("", include("lawrag.apps.engine.urls")),
]

# if apps.is_installed("silk"):
#     urlpatterns.append(path("profiler/", include("silk.urls")))
