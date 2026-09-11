from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    """A hierarchical product category, stored as a nested set via django-mptt."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name_plural = "categories"
        constraints = [
            models.UniqueConstraint(
                fields=["parent", "slug"], name="unique_slug_per_parent"
            )
        ]

    def __str__(self):
        return self.name


class Product(models.Model):
    """A leaf item hanging off a category, to show the tree in a foreign key widget."""

    name = models.CharField(max_length=200)
    category = TreeForeignKey(
        Category, related_name="products", on_delete=models.PROTECT
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
