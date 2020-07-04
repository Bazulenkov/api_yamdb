from django.apps import AppConfig

# from django.db.models.signals import post_save, post_delete
from api.signals import set_title_rating


class ApiConfig(AppConfig):
    name = "api"

    def ready(self):
        # importing model classes
        Title = self.get_model("Review")
        # registering signals with the model's string label
        post_save.connect(set_title_rating, sender=api.Review)
        post_delete.connect(set_title_rating, sender=api.Review)
