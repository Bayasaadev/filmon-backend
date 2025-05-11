from rest_framework import permissions

class isOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: allow full access to owners, read-only for others.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user