from rest_framework import generics, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoriesList(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ["=name", ]


class GenresList(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ["=name", ]


class TitleViewset(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ["=category__slug", "=genres__slug", "=year", "name"]
