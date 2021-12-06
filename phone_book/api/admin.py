from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Company, Employee

User = get_user_model()


class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'address',
        'description',
        'owner',
    )
    list_filter = ('owner', 'name')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'middle_name',
        'position',
        'personal_phone',
        'office_phone',
        'fax',
        'company'
    )
    list_filter = ('company', )


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(User, UserAdmin)
