from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Review(models.Model):
    """ Модель отзывов. Отзыв прявязан к определенному произведению """

    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name=review_title)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name=review_author)
    score = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(_("review date"), auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """ Модель комментариев к отзывам. Комментарий привязан к определённому отзыву. """

    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name=comment_title)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name=comment_review)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name=comment_author)
    pub_date = models.DateTimeField(_("comment date"), auto_now_add=True)

    def __str__(self):
        return self.text
