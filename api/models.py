from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=200)
    rating = models.FloatField(default=None, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="titles")
    genre = models.ManyToManyField(Genre, through="GenreTitle", related_name="titles")

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.PROTECT)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
