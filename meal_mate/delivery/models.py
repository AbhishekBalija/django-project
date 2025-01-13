from django.db import models

# Create your models here.



class Customer(models.Model):
    fullname = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.fullname} {self.email} {self.password} {self.phone} {self.address}"