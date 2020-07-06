from django.db.models import Avg
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from api.models import Review


@receiver([post_save, post_delete], sender=Review)
def set_title_rating(sender, instance, **kwargs):
    title = instance.title
    title.rating = title.reviews.aggregate(Avg("score")).get("score__avg")
    title.save()
