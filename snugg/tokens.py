from rest_framework_simplejwt.tokens import AccessToken, BlacklistMixin, RefreshToken


class RefreshToken(RefreshToken):
    pass


class AccessToken(BlacklistMixin, AccessToken):
    pass
