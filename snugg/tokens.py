from rest_framework_simplejwt.tokens import BlacklistMixin, RefreshToken, AccessToken


class RefreshToken(RefreshToken):
    pass


class AccessToken(BlacklistMixin, AccessToken):
    pass