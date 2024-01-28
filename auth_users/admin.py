from django.contrib import admin

from auth_users.models import Suspend


# Register your models here.
@admin.register(Suspend)
class SuspendAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_date', 'to_date',)
    sortable_by = ('-from_date', '-to_date', 'user')
    search_fields = ('user__username',)

