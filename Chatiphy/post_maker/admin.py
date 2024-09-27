from django.contrib import admin
from .models import Post, Group


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # List of models attributes shown at the interface(pk means PrimaryKey)
    list_display = ("pk", "text", "pub_date", "author", "group")
    # Editing groups in posts list in admin zone
    list_editable = ("group",)
    # List of fields for searching
    search_fields = ("text", "author", "group")
    # List of fields for filtering
    list_filter = ("pub_date",)
    # Value for empty rows in the text fields
    empty_value_display = "--empty--"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug", "description")
    list_editable = ("description",)
    # Auto-add slug field with title text
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "slug", "description")
    list_filter = ("title",)
    empty_value_display = "--empty--"
