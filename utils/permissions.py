from rest_framework import permissions

from utils.make_openid import make_openid


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_superuser




class IsUserOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_permission(self, request, view):
        JSCODE = request.data.get('JSCODE')
        dict_result = make_openid(JSCODE)
        print('dict_result', dict_result)
        if dict_result.get('errmsg'):
            return False
        return True


