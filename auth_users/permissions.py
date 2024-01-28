import datetime

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsNotSuspendedOrReadOnly(BasePermission):
    message = 'You are suspended and cannot perform this action'

    def has_permission(self, request, view):
        now = datetime.datetime.now().date()
        is_suspended = request.user.suspends.filter(to_date__gt=now).exists()
        if request.method in SAFE_METHODS or not is_suspended:
            return True
        return False
