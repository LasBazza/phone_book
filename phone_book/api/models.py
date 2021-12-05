from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models


class CustomUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        validators=[username_validator],
    )
    rights_to_edit_companies = models.ManyToManyField(
        'Company',
        blank=True,
        verbose_name='Компании, которые юзер имеет право редактировать'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Company(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название'
    )
    address = models.CharField(max_length=300, verbose_name='Адрес')
    description = models.TextField(verbose_name='Описание')
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='own_companies',
        verbose_name='Владелец организации',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


class Employee(models.Model):

    PHONE_REGEX = r'^\+\d+$'

    first_name = models.CharField(max_length=200, verbose_name='Имя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия')
    middle_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Отчество'
    )
    company = models.ForeignKey(
        Company,
        related_name='employees',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Организация'
    )
    position = models.CharField(max_length=200, verbose_name='Должность')
    personal_phone = models.CharField(
        max_length=200,
        verbose_name='Личный телефон',
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=PHONE_REGEX, message='Enter correct number start with +'
        )]
    )
    office_phone = models.CharField(
        max_length=200,
        verbose_name='Рабочий телефон',
        blank=True,
        validators=[RegexValidator(
            regex=PHONE_REGEX, message='Enter correct number start with +'
        )]
    )
    fax = models.CharField(
        max_length=200,
        verbose_name='Факс',
        blank=True,
        validators=[RegexValidator(
            regex=PHONE_REGEX, message='Enter correct number start with +'
        )]
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
