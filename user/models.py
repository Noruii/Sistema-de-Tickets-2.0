from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# Asignar la imagen por defecto si el campo avatar está vacío
from django.core.files import File
# from django.conf import settings
from pathlib import Path

# Create your models here.
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, matricula, password=None, **extra_fields):
        if not matricula:
            raise ValueError('El campo matricula es obligatorio.')
        user = self.model(matricula=matricula, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matricula, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Los superusuarios deben tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Los superusuarios deben tener is_superuser=True.')

        return self.create_user(matricula, password, **extra_fields)

# Modelo user personalizado aumentando campos
class User(AbstractUser):
    matricula = models.CharField(
        max_length=10, 
        unique=True
    )
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'matricula'

    def get_default_image_path():
        default_image_path = None
        static_dirs = settings.STATICFILES_DIRS
        # Iterar sobre cada directorio en STATICFILES_DIRS
        for static_dir in static_dirs:
            # Buscar el archivo en cada directorio
            image_path = Path(static_dir) / 'img/user_icon.png'
            if image_path.exists():
                default_image_path = image_path
                break  # Detenerse si se encuentra la imagen
        return default_image_path

    def save(self, *args, **kwargs):
        # Verificar si el campo avatar está vacío o es None
        if not self.avatar:
            # Ruta de la imagen por defecto
            def get_default_image_path():
                default_image_path = None
                static_dirs = settings.STATICFILES_DIRS
                # Iterar sobre cada directorio en STATICFILES_DIRS
                for static_dir in static_dirs:
                    # Buscar el archivo en cada directorio
                    image_path = Path(static_dir) / 'img/user_icon.png'
                    if image_path.exists():
                        default_image_path = image_path
                        break  # Detenerse si se encuentra la imagen
                return default_image_path
            default_image_path = get_default_image_path()
            # Abrir y asignar la imagen por defecto al campo avatar
            with open(default_image_path, 'rb') as f:
                self.avatar.save('user_icon.png', File(f), save=False)
        super().save(*args, **kwargs)
    
    def get_image(self):
        if self.avatar:
            return '{}{}'.format(settings.MEDIA_URL, self.avatar)
        return '{}{}'.format(settings.STATIC_URL, 'img/user_icon.png')
