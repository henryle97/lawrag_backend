from django.utils.translation import gettext_lazy
from drf_spectacular.utils import (
    OpenApiResponse,
    PolymorphicProxySerializer,
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from lawrag.apps.engine.models import User
from lawrag.apps.engine.serializers.users import UserSerializer


@extend_schema(tags=["users"])
@extend_schema_view(
    list=extend_schema(
        summary="Method provides a paginated list of users registered in the server"
    ),
    retrieve=extend_schema(
        summary="Method provides a detailed information about a specific user",
        responses={
            "200": PolymorphicProxySerializer(
                component_name="MetaUser",
                serializers=[UserSerializer],
                resource_type_field_name="username",
            )
        },
    ),
    partial_update=extend_schema(
        summary="Method allows to update a specific user",
        responses={
            "200": PolymorphicProxySerializer(
                component_name="MetaUser",
                serializers=[UserSerializer],
                resource_type_field_name="username",
            )
        },
    ),
    destroy=extend_schema(
        summary="Method allows to delete a specific user",
        responses={
            "204": OpenApiResponse(description="User deleted successfully")
        },
    ),
)
class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = User.objects.prefetch_related("groups").all()
    ttp_method_names = ["get", "post", "head", "patch", "options"]

    def get_serializer_class(self):
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return self.queryset
        elif self.action == "self":
            return self.queryset.filter(id=user.id)
        elif self.action == "list":
            return self.queryset.filter(is_active=True)
        elif self.action == "retrieve":
            if user.id == int(self.kwargs.get("pk", 0)):
                return self.queryset.filter(id=user.id)
            else:
                raise ValidationError(
                    gettext_lazy(
                        "You do not have permissions to access this user"
                    )
                )
        else:
            return self.queryset.none()

    @extend_schema(
        summary="Method returns an instance of a user who is currently authorized",
        responses={
            "200": PolymorphicProxySerializer(
                component_name="MetaUser",
                serializers=[
                    UserSerializer,
                ],
                resource_type_field_name="username",
            ),
        },
    )
    @action(detail=False, methods=["GET"])
    def self(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            request.user, context={"request": request}
        )
        return Response(serializer.data)

    def perform_destroy(self, instance):
        num_active_superusers = (
            User.objects.filter(is_superuser=True)
            .filter(is_active=True)
            .count()
        )
        if num_active_superusers == 1 and instance.is_superuser:
            raise ValidationError(
                gettext_lazy("You cannot delete the last active superuser")
            )
        instance.delete()
