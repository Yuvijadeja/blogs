from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - SAFE methods (GET, HEAD, OPTIONS) → allow for everyone
    - POST → allow only authenticated
    - PUT/PATCH/DELETE → allow only the author
    """
    def has_permission(self, request, view):
        # Allow anyone to read
        if request.method in permissions.SAFE_METHODS:
            return True
        # Require authentication for write actions
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # SAFE methods → always allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only author can edit/delete
        return obj.author == request.user
