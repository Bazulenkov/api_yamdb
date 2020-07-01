from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    """ Модель отзывов. Отзыв прявязан к определенному произведению """

    title = models.ForeignKey("Title", on_delete=models.CASCADE, related_name=reviews)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name=reviews)
    score = models.PositiveSmallIntegerField(help_text="Введите оценку от 1 до 10")
    pub_date = models.DateTimeField(_("review date"), auto_now_add=True)

    class Meta:
        unique_together = ["title", "author"]
        ordering = ["pub_date"]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """ Модель комментариев к отзывам. Комментарий привязан к определённому отзыву. """

    title = models.ForeignKey("Title", on_delete=models.CASCADE, related_name=comments)
    review = models.ForeignKey("Review", on_delete=models.CASCADE, related_name=comments)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name=comments)
    pub_date = models.DateTimeField(_("comment date"), auto_now_add=True)

    class Meta:
        ordering = ["pub_date"]

    def __str__(self):
        return self.text
