import re

from django.contrib.auth import get_user_model
from rest_framework.permissions import DjangoObjectPermissions

SAFE_PERM_TYPES = ("view",)


class FullObjectPermissions(DjangoObjectPermissions):
    """
    Similar to `DjangoObjectPermissions`, but adding 'view' permissions.
    """

    perms_map = {
        "GET": ["%(app_label)s.view_%(model_name)s"],
        "OPTIONS": ["%(app_label)s.view_%(model_name)s"],
        "HEAD": ["%(app_label)s.view_%(model_name)s"],
        "POST": ["%(app_label)s.add_%(model_name)s"],
        "PUT": ["%(app_label)s.change_%(model_name)s"],
        "PATCH": ["%(app_label)s.change_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }

    def has_permission(self, request, view):
        """
        We don't check model permission here.
        Other permission classes such as "IsAuthenticatedOrReadOnly" would do it.
        """
        return True


class ObjectPermissionsBackend:
    """
    Object-level permissions backend that checks whether the requesting user is
    the owner of the object, and whether the object is private.

    All the permissions are granted to the owner of the object, and only
    limited permissions are granted to the other users. If the object is set to
    'private', this does not grant any permissions to users other than the
    owner.

    Unlike 'django-guardian', this does not require any permissions assigning
    process. This means that there is no database query in the process of
    checking permissions.
    """

    is_private_field = "is_private"

    owner_field_map = {
        "qna.post": "writer",
        "qna.answer": "writer",
        "qna.comment": "writer",
        "agora.post": "writer",
        "media.directory": "uploader",
    }

    def authenticate(self, *args, **kwargs):
        """
        django.contrib.auth.backends.ModelBackend would do the job.
        """
        pass

    def get_owner_field(self, obj):
        app_label = obj._meta.app_label
        model_name = obj._meta.model_name
        key = f"{app_label}.{model_name}"

        return self.owner_field_map.get(key, None)

    def get_perm_type(self, perm):
        """
        This might not be robust enough.
        """
        pattern = re.compile("\.(view|add|change|delete)\_")
        match = pattern.search(perm)

        # Pattern not found.
        if match is None:
            return None

        # Remove leading period and trailing underscore.
        perm_type = match.group(0)[1:-1]

        return perm_type

    # TODO: test anonymous user.
    def has_perm(self, user, perm, obj=None):
        # Not dealing with non-object permissions.
        if obj is None:
            return True

        perm_type = self.get_perm_type(perm)

        # If obj is an instance of 'User' model,
        # check if the object is same as the user.
        if obj._meta.model is get_user_model():
            if perm_type in SAFE_PERM_TYPES:
                return True
            return user == obj

        owner_field = self.get_owner_field(obj)
        is_private = getattr(obj, self.is_private_field, False)

        # If there is no owner field, use 'is_private' field to check permission.
        if owner_field is None:
            return not is_private

        # Main permission check logic starts here.
        is_owner = getattr(obj, owner_field) == user

        if is_owner:
            return True

        if is_private:
            return False
        else:
            if perm_type in SAFE_PERM_TYPES:
                return True
            else:
                return False


# TODO: PrivateFilterBackend - filter queryset by checking the private object's owner is the requesting user.
