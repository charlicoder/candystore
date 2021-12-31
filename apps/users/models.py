from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.
class CandyUserManager(BaseUserManager):
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

    # Method called while calling createsuperuser
    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.save_user(email, password, **extra_fields)


SIGNUP_STATUS = (
    ('new', 'new'),
    ('email_verified', 'Email Verified'),
    ('documents_uploaded', 'Documents Uploaded'),
    ('doc_verified', 'Document Verified'),
    ('doc_not_verified', 'Document Not Verified'),
    ('agreement_signed', 'Agreement Signed'),
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('on_hold', 'On Hold'),
)


class CandyUserRole(models.Model):
    role_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.role_name


# Create your models here.
class CandyUser(AbstractBaseUser, PermissionsMixin):
    # Email field that serves as the username field
    email = models.EmailField(max_length=50, unique=True, verbose_name="Email")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.ForeignKey(CandyUserRole, blank=True, null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=SIGNUP_STATUS, default=SIGNUP_STATUS[0])
    
    # Setting email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Custom user manager
    objects = CandyUserManager()

    def __str__(self):
        return self.email
    

# class UserEmailVerifyToken(models.Model):
#     user = models.OneToOneField(CandyUser, editable=False, on_delete=models.CASCADE)
#     token = models.CharField(max_length=100, blank=False, null=False, unique=True, editable=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=(('new', 'New'), ('verified', 'Verified')))


class CandyUserProfile(models.Model):
    user = models.OneToOneField(CandyUser, editable=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    def __str__(self):
        return self.user.email

    def get_full_name(self):
        # Returns the first_name plus the last_name, with a space in between.
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        # Returns the short name for the user.
        return self.first_name


CONTACT_TYPE = (
    ('email', 'Email'),
    ('mobile', 'Mobile'),
    ('skype', 'Skype'),
    ('telegram', 'Telegram'),
    ('whatsapp', 'WhatsApp'),
)


class CandyUserContact(models.Model):
    user = models.ForeignKey(CandyUser, on_delete=models.CASCADE)
    contact_type = models.CharField(max_length=24, choices=CONTACT_TYPE, default='email')
    contact_id = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.contact_id
