from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from api.models import Review, Title


@receiver([post_save, post_delete], sender=Review)
def set_title_rating(sender, **kwargs):
    title = generics.get_object_or_404(Title, id=kwargs.get('title_id')
    title.rating = (
        title.reviews.aggregate(Avg("score")).get("score__avg")
    )
    title.save()
