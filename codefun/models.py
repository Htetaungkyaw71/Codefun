from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    otp = models.CharField(max_length=64)
    is_email = models.BooleanField(default=False)

class Code(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="coder")
    name = models.CharField(max_length=64)
    text = models.TextField()
    postchoice = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True,auto_created=True)

    def __str__(self):
        return f"{self.text}"

