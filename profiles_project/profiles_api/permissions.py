from rest_framework import permissions


class UserOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profiles"""

    def has_object_permission(self, request, view, obj):
        """check if user is trying to edit their own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.id == obj.id
