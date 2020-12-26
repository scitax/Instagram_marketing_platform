from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Platforms, Add_posting


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'last_login', 'usertype')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_admin',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2', 'usertype')
            }
        ),
    )

    list_display = ('email', 'username', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_admin', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
admin.site.register(Platforms)
admin.site.register(Add_posting)