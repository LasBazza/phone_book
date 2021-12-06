from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from .models import Company


class SignUpOrIsAuthentificatedOrSelf(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method == 'POST' or
                request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                request.user == obj)


class IsCompanyOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
                request.user == obj.owner)


class HasRigthsToEditOrReadOnly(permissions.BasePermission):
    message = ('You do not have rights to edit employees data '
               'in this company')

    def _rights_pattern(self, request, obj):
        if request.user.is_authenticated:
            return (obj in request.user.rights_to_edit_companies.all() or
                    obj.owner == request.user)
        return False

    def has_permission(self, request, view):
        company_id = request.data.get('company')

        if company_id:
            try:
                company = Company.objects.get(id=company_id)
            except ObjectDoesNotExist:
                return True
            rights = self._rights_pattern(request, company)
        else:
            rights = True
        return request.method in permissions.SAFE_METHODS or rights

    def has_object_permission(self, request, view, obj):
        company = obj.company
        return (request.method in permissions.SAFE_METHODS or
                self._rights_pattern(request, company))
