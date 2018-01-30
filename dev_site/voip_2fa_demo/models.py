from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField("Name", max_length=127)
    user_email = models.CharField("Email", max_length=255, unique=True)
    user_salt = models.CharField(max_length=15)
    user_password_hash = models.CharField(max_length=255)
    user_phone_number = models.CharField("Phone Number", max_length=32)
    user_2FA_code = models.CharField(max_length=15)
    user_is_admin = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_id) + ": " + \
               self.user_name + ": " + self.user_email

