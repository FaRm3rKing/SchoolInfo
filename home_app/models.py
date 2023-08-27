from django.db import models
# accounts/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, role, password=None):
        if not email:
            raise ValueError("Please provide an email address")

        user = self.model(
            email=self.normalize_email(email),
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, role="admin", password=None):
        user = self.create_user(
            email=email,
            role=role,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    # add additional fields in here
    TEACHER = "teacher"
    STUDENT = "student"
    ROLE_CHOICES = ((TEACHER, "Teacher"),
                    (STUDENT, "Student")
                   )
    email = models.EmailField(max_length=255, unique=True)
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default="Student")

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"


    # the required fields when creating a superuser
    # do not include USERNAME_FIELD or password
    # REQUIRED_FIELDS = ["email"]
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

