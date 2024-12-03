
# accounts/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('メールアドレスは必須です')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('スーパーユーザーはis_staff=Trueでなければなりません')
        if not extra_fields.get('is_superuser'):
            raise ValueError('スーパーユーザーはis_superuser=Trueでなければなりません')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    twitter_username = models.CharField('Twitterユーザー名', max_length=50, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField('タイトル', max_length=255)
    target_date = models.DateField('目標日', null=True, blank=True)
    target_hours = models.FloatField('目標時間（h）', null=True, blank=True)
    start_tag = models.CharField('開始タグ', max_length=50, default='#開始')
    end_tag = models.CharField('終了タグ', max_length=50, default='#終了')
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    def __str__(self):
        return self.title

class StudySession(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='sessions')
    start_time = models.DateTimeField('開始時間')
    end_time = models.DateTimeField('終了時間')
    duration = models.FloatField('継続時間（時間）')

    def __str__(self):
        return f"{self.task.title} - {self.duration}時間"

