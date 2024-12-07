from django.db import models
from django.core.exceptions import ObjectDoesNotExist

"""
OrderField is a custom field built on PositiveIntegerField to provide:
    1. Automatic assignment of an order value when no specific order is provided.
    2. Ordering of objects with respect to other fields.
"""


class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        """
        :param for_fields: Fields to group ordering by (e.g., 'course' or 'module').
        """
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        Automatically assigns an order value if one is not provided.

        :param model_instance: The model instance being saved.
        :param add: Boolean indicating whether the instance is being added.
        """
        # If the order field is not set, assign it automatically
        if getattr(model_instance, self.attname) is None:
            try:
                # Get all objects of the model
                qs = self.model.objects.all()

                # Filter the query set by for_fields if specified
                if self.for_fields:
                    query = {
                        field: getattr(model_instance, field) for field in self.for_fields
                    }
                    qs = qs.filter(**query)

                # Retrieve the latest object by order and increment
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                # If no objects exist, start with 0
                value = 0

            # Assign the calculated value to the field
            setattr(model_instance, self.attname, value)
            return value
        else:
            # Use the manually assigned order value
            return super().pre_save(model_instance, add)
