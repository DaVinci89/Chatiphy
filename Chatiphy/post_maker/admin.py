from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    # List of models attributes shown at the interface(pk means PrimaryKey)
    list_display = ("pk", "text", "pub_date", "author")
    # List of fields for searching
    search_fields = ("text",)
    # List of fields for filtering
    list_filter = ("pub_date",)
    # Value for empty rows in the text fields
    empty_value_display = "--empty--"


admin.site.register(Post, PostAdmin)
