from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """ Checks if user is an owner """

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False


class IsTheUser(permissions.BasePermission):
    """ Checks if the user is the user(owner) to retrieve and update own profile"""

    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        return False

"""
    def has_obj_permission(self, request, view, obj):
        print(request)
        print(view)
        print(obj)
        if obj.id == request.user.id:
            return True
        else:
            return False"""


class IsAdmin(permissions.BasePermission):
    """ Checks if user is an admin """

    def has_permission(self, request, view):
        if request.user.role == "Администратор":
            return True
        return False
