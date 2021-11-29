from django.db import models

# Create your models here.
from django.utils import timezone


class Users(models.Model):
    user_uuid = models.CharField(max_length=400, blank=False, null=False, unique=True)
    is_banned = models.BooleanField(blank=False, null=False, default=False)
    last_visited = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.user_uuid


class Domain(models.Model):
    domain = models.CharField(max_length=200, null=False, unique=True)

    class Meta:
        verbose_name = 'Domain'
        verbose_name_plural = 'Domains'

    def __str__(self):
        return self.domain


class URLs(models.Model):
    user_uuid = models.ForeignKey(Users, on_delete=models.CASCADE, default=None)
    domain = models.ForeignKey(Domain,
                               default=1,
                               on_delete=models.CASCADE)
    url = models.CharField(max_length=200, null=False)
    url_destination = models.CharField(max_length=500, null=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'URL'
        verbose_name_plural = 'URLs'

        unique_together = ['domain', 'url', 'url_destination']

    def __str__(self):
        return self.domain.domain + '/' + self.url



