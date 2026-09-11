# django-mptt-admin example

A minimal Django project showing [django-mptt-admin](https://github.com/mbraak/django-mptt-admin):
a drag-and-drop tree interface in the Django admin for
[django-mptt](https://github.com/django-mptt/django-mptt) models.

The example app is `catalog`, with a hierarchical `Category` tree and a flat `Product`
model that points into the tree.

## Run it

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_catalog      # demo tree, products and an admin user
python manage.py runserver
```

Then open <http://127.0.0.1:8000/admin/> and log in with `admin` / `admin`.

Go to **Catalog › Categories** to see the tree. You can:

- drag nodes to reorder them or move them under another parent
- right-click a node for a context menu (add child, edit, delete)
- filter the tree by *is active* in the sidebar
- switch to the regular list view with the "grid view" link, and back again

Pass `--reset` to `seed_catalog` to wipe and recreate the demo data.

## Linting

The project is configured for [ruff](https://docs.astral.sh/ruff/) in `ruff.toml`.

```bash
pip install -r requirements-dev.txt
ruff check .
ruff format .
```

## Where to look

| File | What it shows |
| --- | --- |
| `catalog/models.py` | `Category(MPTTModel)` with a `TreeForeignKey` parent and `MPTTMeta.order_insertion_by` |
| `catalog/admin.py` | `CategoryAdmin(DjangoMpttAdmin)` and the options it configures |
| `config/settings.py` | `mptt`, `django_mptt_admin` and `catalog` in `INSTALLED_APPS` |
| `catalog/management/commands/seed_catalog.py` | Bulk-creating a tree with `disable_mptt_updates()` and `rebuild()` |

## Admin options used

```python
class CategoryAdmin(DjangoMpttAdmin):
    item_label_field_name = "name"   # field used as the node label (default: str(obj))
    tree_auto_open = 1               # levels expanded on first load
    tree_load_on_demand = 1          # load deeper levels lazily over AJAX
    use_context_menu = True          # right-click menu on nodes
    list_filter = ("is_active",)     # shown in tree view and grid view
    list_display = (...)             # grid view only
```

Other useful attributes on `DjangoMpttAdmin`: `trigger_save_after_move` (call `save()`
after a drag, so `post_save` handlers run), `autoescape`, `tree_animation_speed`,
`tree_mouse_delay`. Override `get_tree_data()` or `do_move()` to customise the JSON
sent to the tree or the move behaviour.

## Versions this was built against

- Django 6.1
- django-mptt 0.18
- django-mptt-admin 3.0
