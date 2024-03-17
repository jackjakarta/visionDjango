from django.contrib.auth.models import BaseUserManager


class AuthUserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, is_social_auth=False, **kwargs):
        if not first_name:
            raise ValueError('Users must have a first name.')

        if not last_name:
            raise ValueError('Users must have a last name.')

        if not email:
            raise ValueError('User must have email addresses!')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email)
        )
        user.is_social_auth = is_social_auth
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name=None, last_name=None):
        user = self.create_user(email, first_name, last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user
    