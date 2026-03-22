from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class ApplicationUser(AbstractUser):
    
    username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True,unique=True)
    nid = models.CharField(max_length=40, blank=False, null=False,unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    user_Type = models.CharField(max_length=20,null=False, blank=False,default='Not Set', choices=(('Patient','Patient'),('Doctor', 'Doctor'),('Admin','Admin'),('Not Set', 'Not Set')))
    user_id= models.BigIntegerField(null=False,blank=False,default=0)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS= ['email','phone_number','nid']
    
    class Meta:
        verbose_name = 'User'
        
        
    def __str__(self):
        return self.username or self.email or self.phone_number or self.nid or 'Unnamed User'
        
