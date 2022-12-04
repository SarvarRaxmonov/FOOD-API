from rest_framework.permissions import BasePermission


class OnlyPersonalUserPermision(BasePermission):
    message = "Uzur siz bu malumotlarga kira olmaysiz"
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
           return True
        return bool(str(obj.user) == str(request.user))
