from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("이름을 설정해주세요.")
        if not email:
            raise ValueError("이메일을 설정해주세요.")

        extra_fields["is_active"] = True
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(force_insert=True, using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields["is_staff"] = False
        extra_fields["is_superuser"] = False
        extra_fields["is_admin"] = False

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["is_admin"] = True

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    objects = CustomUserManager()
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=30, null=False)
    profile_image = models.ImageField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    birth_date = models.DateField(null=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
