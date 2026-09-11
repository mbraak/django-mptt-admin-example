from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from catalog.models import Category, Product

TREE = {
    "Electronics": {
        "Computers": {"Laptops": {}, "Desktops": {}, "Tablets": {}},
        "Phones": {"Smartphones": {}, "Accessories": {}},
        "Audio": {"Headphones": {}, "Speakers": {}},
    },
    "Home & Garden": {
        "Furniture": {"Sofas": {}, "Tables": {}, "Chairs": {}},
        "Kitchen": {"Cookware": {}, "Appliances": {}},
        "Garden": {},
    },
    "Books": {
        "Fiction": {"Science Fiction": {}, "Mystery": {}},
        "Non-fiction": {"History": {}, "Science": {}},
    },
}

PRODUCTS = [
    ("Laptops", "ThinkBook 14", "899.00"),
    ("Laptops", "AirLight 13", "1199.00"),
    ("Smartphones", "Pixelphone 9", "699.00"),
    ("Headphones", "Quiet Cans", "249.00"),
    ("Sofas", "Three-seater linen sofa", "1450.00"),
    ("Cookware", "Cast iron skillet", "39.95"),
    ("Science Fiction", "Dune", "12.50"),
    ("History", "SPQR", "16.00"),
]


class Command(BaseCommand):
    help = "Create demo categories, products and an admin user (admin / admin)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset", action="store_true", help="Delete existing data first."
        )

    def handle(self, *args, **options):
        if options["reset"]:
            Product.objects.all().delete()
            Category.objects.all().delete()

        if Category.objects.exists():
            self.stdout.write("Categories already exist; use --reset to recreate.")
        else:
            with Category.objects.disable_mptt_updates():
                self._create_level(TREE, parent=None)
            Category.objects.rebuild()
            self.stdout.write(f"Created {Category.objects.count()} categories.")

            for category_name, product_name, price in PRODUCTS:
                Product.objects.create(
                    name=product_name,
                    category=Category.objects.get(name=category_name),
                    price=Decimal(price),
                )
            self.stdout.write(f"Created {Product.objects.count()} products.")

        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin")
            self.stdout.write("Created superuser admin / admin.")

    def _create_level(self, nodes, parent):
        for name, children in nodes.items():
            node = Category.objects.create(name=name, slug=slugify(name), parent=parent)
            self._create_level(children, parent=node)
