from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to super_user.
    Custom 관리자 권한 (SuperUser Check)
    """

    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


class IsAuthorOrReadOnly(permissions.BasePermission):
    """작성자만 수정,삭제 가능 권한"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
