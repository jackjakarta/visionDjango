from django.contrib.auth.models import BaseUserManager


class AuthUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have email address.')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True

        user.set_password(password)
        user.save(using=self._db)

        return user
