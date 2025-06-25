from rest_framework import permissions


class IsCreator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Only allow access if the user is the owner of the object
        return obj.creator == request.user