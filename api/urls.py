from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TitleViewset, GenresList, GenreDestroy, CategoriesList, CategoryDestroy

router = DefaultRouter()
router.register("titles", TitleViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('categories/', CategoriesList.as_view()),
    path('categories/<slug>/', CategoryDestroy.as_view()),
    path('genres/', GenresList.as_view()),
    path("genres/<slug>/", GenreDestroy.as_view()),
]
