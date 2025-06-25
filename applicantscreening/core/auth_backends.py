
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from core.models import User as DBUser


class DBUserBackend(BaseBackend):
    """Let Django’s session framework work with our custom *user* table."""

    def authenticate(self, request, username: str = None, password: str = None):
        try:
            db_user = DBUser.objects.get(email=username)
        except DBUser.DoesNotExist:
            return None

        hash_ok = db_user.password == password   # ← replace with real hash check
        if not hash_ok:
            return None

        # We don’t want to duplicate rows in auth_user – so we build an
        # in-memory user object that satisfies request.user.*
        DjangoUser = get_user_model()
        dummy = DjangoUser(id=db_user.id, email=db_user.email,
                           is_staff=(db_user.role != "Job Seeker"),
                           is_superuser=(db_user.role == "Admin"))
        dummy.backend = "core.auth_backends.DBUserBackend"
        dummy.role = db_user.role         # convenience attribute
        return dummy

    def get_user(self, user_id):
        try:
            return self.authenticate(None, DBUser.objects.get(id=user_id).email,
                                     None)
        except DBUser.DoesNotExist:
            return AnonymousUser()
