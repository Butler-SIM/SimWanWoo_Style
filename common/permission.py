from rest_framework import permissions


class IpPermission(permissions.BasePermission):
    """
    IP 관련 권한
    """

    ALLOWED_IP_ADDRESSES = []

    def has_permission(self, request, view):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(",")[0]
        else:
            ip_address = request.META.get("REMOTE_ADDR")

        return ip_address in self.ALLOWED_IP_ADDRESSES


class ImportPermission(IpPermission):
    """
    아임포트 IP 권한
    """

    ALLOWED_IP_ADDRESSES = ["52.78.100.19", "52.78.48.223"]


class ShippingPermission(IpPermission):
    """
    배송 관련 권한
    """

    ALLOWED_IP_ADDRESSES = ["배송업체 IP"]


class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to super_user.
    Custom 관리자 권한 (SuperUser Check)
    """

    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """작성자만 수정,삭제 가능 권한"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
