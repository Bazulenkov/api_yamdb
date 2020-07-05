from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework import generics

from api.models import Review, Title


@receiver(post_save, sender=Review)
def set_title_rating(sender, instance, **kwargs):
    print("signal")
    if score in kwargs.get("update_fields"):
        title = kwargs.get("instance").title
        # title = Title.objects.get(id=kwargs.get('title_id')
        title.rating = title.reviews.aggregate(Avg("score")).get("score__avg")
        title.save()
