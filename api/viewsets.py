from rest_framework import filters, mixins, viewsets

from api.permissions import IsAdminOrReadOnly


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = [
        "=name",
    ]
