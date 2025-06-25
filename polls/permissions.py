from rest_framework import permissions


class IsCreatorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Only allow access if the user is the owner of the object
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user