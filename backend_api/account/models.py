from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, name, and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        username = email.split('@')[0]  # Extract the part before '@' for username

        user = self.model(
            email=email,
            username=username,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, name, and password.
        """
        user = self.create_user(
            email=email,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

USER_ROLE = [
    ('ADMINS', 'Admins'),
    ('USERS', 'Users'),
]

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    # username = models.CharField(max_length=100, unique=True,null=True,blank=True)
    name = models.CharField(max_length=200)
    user_role = models.CharField(max_length=15, choices=USER_ROLE, default='USERS')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
    
    @property
    def username(self):
        return self.email.split('@')[0]
    
    # def save(self, *args, **kwargs):
    #     # Automatically set the username to the part before '@' in the email
    #     if not self.username:
    #         self.username = self.email.split('@')[0]
    #     super().save(*args, **kwargs)