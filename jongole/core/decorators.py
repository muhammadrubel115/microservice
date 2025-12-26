from rest_framework.response import Response
from rest_framework import status


def require_permission(permission):
    def decorator(view_func):
        def wrapped(self, request, *args, **kwargs):
            perms = getattr(request, "permissions", [])
            if permission not in perms:
                return Response(
                    {"detail": "Forbidden"},
                    status=status.HTTP_403_FORBIDDEN,
                )
            return view_func(self, request, *args, **kwargs)
        return wrapped
    return decorator
