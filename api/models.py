from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="titles"
    )
    genre = models.ManyToManyField(
        Genre, through="GenreTitle", related_name="titles"
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.PROTECT)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT)


class Review(models.Model):
    """ Модель отзывов. Отзыв прявязан к определенному произведению """

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.PositiveSmallIntegerField(
        help_text="Введите оценку от 1 до 10"
    )
    pub_date = models.DateTimeField("review date", auto_now_add=True)

    class Meta:
        unique_together = ["title", "author"]
        ordering = ["pub_date"]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """ Модель комментариев к отзывам. Комментарий привязан к определённому отзыву. """

    title = models.ForeignKey(
        "Title", on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        "Review", on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField("comment date", auto_now_add=True)

    class Meta:
        ordering = ["pub_date"]

    def __str__(self):
        return self.text
