from django.contrib import admin

from bake_cake_bot.models import Users


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'username', 'name', 'is_admin']
    search_fields = ['telegram_id', 'username', 'phone']
