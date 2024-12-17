from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile

# Inline профілю для редагування разом із користувачем
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Перевизначення адмінки для User
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

# Реєстрація моделі Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'date_of_birth', 'location')  # Поля для відображення у списку профілів

# Перереєстрація User для інтеграції з Profile
admin.site.unregister(User)
admin.site.register(User, UserAdmin)