from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class AccountAdmin(UserAdmin):
    list_display = ('email', 'name', 'surname', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'name', 'surname')
    readonly_fields = ('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'name', 'surname', 'date_joined', 'last_login')}),
        ('Permissions', {'fields':('is_admin', 'is_staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'surname', 'password1', 'password2'),
        }),
    )

    # tuple, need comma
    ordering = ('email',)


admin.site.register(Account, AccountAdmin)
