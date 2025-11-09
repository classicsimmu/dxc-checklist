from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    fk_name = 'user'
    can_delete = False
    verbose_name_plural = 'Profile'
    extra = 1      # add form par 1 blank inline dikhane do
    max_num = 1    # sirf ek hi profile allow

    def has_add_permission(self, request, obj):
        # change page par agar profile already hai to naya add mat dikhana
        if obj and hasattr(obj, 'profile'):
            return False
        return True

class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff', 'is_active')

    def get_role(self, obj):
        try:
            return obj.profile.role
        except Profile.DoesNotExist:
            return '-'
    get_role.short_description = 'Role'

# default User admin ko replace karo
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
