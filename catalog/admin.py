from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    """Tree view with drag-and-drop, plus the regular grid view via the toggle link."""

    # Column shown for each node in the tree; defaults to str(obj).
    item_label_field_name = "name"

    # Open the first level on load; load deeper levels lazily via AJAX.
    tree_auto_open = 1
    tree_load_on_demand = 1

    # Right-click context menu on nodes (add child, edit, delete).
    use_context_menu = True

    # Filters appear in both the tree view and the grid view.
    list_filter = ("is_active",)

    # Options used by the grid (list) view.
    list_display = ("name", "slug", "is_active", "level")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")
    list_filter = ("category",)
    search_fields = ("name",)
    autocomplete_fields = ("category",)
