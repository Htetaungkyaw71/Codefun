from django.core.exceptions import PermissionDenied
from .models import Code, User


def currentuser_is_entry_author(function):
    def wrap(request, *args, **kwargs):
        profile = User.objects.filter(username=request.user.username).first()
        if not profile:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap