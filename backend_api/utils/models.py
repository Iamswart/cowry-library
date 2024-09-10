from django.db import models


class DatesMixin(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def update_model(model: models.Model, data: dict):
    for key, value in data.items():
        if hasattr(model, key):
            setattr(model, key, value)
