from rest_framework import generics, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .filters import TitleFilter
from .models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoriesList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ["=name", ]


class CategoryDestroy(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


class GenresList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ["=name", ]


class GenreDestroy(generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filterset_class = TitleFilter
    filter_backends = [DjangoFilterBackend, ]
    ordering_fields = ["name"]

    def perform_create(self, serializer):
        category = generics.get_object_or_404(Category, slug=self.request.data.get("category"))
        genre = Genre.objects.filter(slug__in=self.request.data.getlist("genre"))
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        title = self.get_object()
        category = generics.get_object_or_404(Category, slug=self.request.data.get("category"))
        genre = Genre.objects.filter(slug__in=self.request.data.getlist("genre"))
        title.genre.set(genre)
        serializer.save()
        title.category = category
        #title.save()
        #serializer.save()