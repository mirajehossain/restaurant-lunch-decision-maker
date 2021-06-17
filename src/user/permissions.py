from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.is_superuser


class IsRestaurantOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return 'RestaurantOwner' in request.groups

