from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Allows access only to the owner of the object, for all HTTP methods.
    """

    def has_permission(self, request, view):
        # Allow access only if user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow access only if the user is the owner of the object
        return hasattr(obj, 'user') and obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """    
    def has_permission(self, request, view):
        # Allow read-only permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Otherwise, ensure the user is authenticated
        return request.user and request.user.is_authenticated
    
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet
        return obj.user == request.user