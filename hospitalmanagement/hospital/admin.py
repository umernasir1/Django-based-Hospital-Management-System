from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin

# Unregister the default Group admin to avoid conflicts
admin.site.unregister(Group)

# Custom Group admin with user count display
class CustomGroupAdmin(GroupAdmin):
    list_display = ('name', 'get_user_count')

    def get_user_count(self, obj):
        return obj.user_set.count()
    get_user_count.short_description = 'Users'

# Register the customized Group admin
admin.site.register(Group, CustomGroupAdmin)
