from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # خواندن برای همه مجاز است
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # نویسنده یا ادمین می‌تواند ویرایش کند
        return obj.author == request.user or request.user.is_admin()

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin()