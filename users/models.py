from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    # Method to save user to the database
    def save_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # Call this method for password hashing
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        extra_fields['is_active'] = False
        return self.save_user(email, password, **extra_fields)

    # Method called while creating a staff user
    def create_staffuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_active'] = True
        extra_fields['is_superuser'] = False
        
        return self.save_user(email, password, **extra_fields) 

    # Method called while calling creatsuperuser
    def create_superuser(self, email, password, **extra_fields):

        # Set is_superuser parameter to true
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser should be True')
        
        extra_fields['is_staff'] = True
        extra_fields['is_active'] = True

        return self.save_user(email, password, **extra_fields)




SIGNUP_STATUS = (
    ('new', 'new'),
    ('email_verified', 'Email Verified'),
    ('documents_uploaded', 'Documents Uploaded'),
    ('id_verified', 'ID Verified'),
    ('id_not_verified', 'ID Not Verified'),
    ('agreement_signed', 'Agreement Signed'),
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('on_hold', 'On Hold'),
)

# Create your models here.
class CandyUser(AbstractBaseUser, PermissionsMixin):
    # Email field that serves as the username field
    email = models.EmailField(max_length = 50, unique = True, verbose_name = "Email")

    # Other required fields for authentication
    # If the user is a staff, defaults to false
    is_staff = models.BooleanField(default=False)
    
    # If the value is set to false, user will not be allowed to sign in.
    is_active = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=SIGNUP_STATUS, default=SIGNUP_STATUS[0])
    
    # Setting email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Custom user manager
    objects = UserManager()

    def __str__(self):
        return self.email
    

class UserEmailVeirfyToken(models.Model):
    user = models.OneToOneField(CandyUser, editable=False, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, blank=False, null=False, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=(('new', 'New'), ('verified', 'Verified')))


class CandyUserProfile(models.Model):
    user = models.OneToOneField(CandyUser, editable=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    avater = models.ImageField(upload_to='avatars', blank=True, null=True)

    def __str__(self):
        return self.user.email

    def get_full_name(self):
        # Returns the first_name plus the last_name, with a space in between.
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        # Returns the short name for the user.
        return self.first_name


