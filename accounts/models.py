from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('Staff', 'Staff'),
        ('Doer', 'Doer'),
    )

    DEPARTMENT_CHOICES = (
        ('MDO', 'MDO'),
        ('Accounts', 'Accounts'),
        ('CRM', 'CRM'),
        ('Sales', 'Sales'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=30, choices=DEPARTMENT_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
