from rest_framework import serializers 
from users.models import ApplicationUser

class ApplicationUserSerializer(serializers.ModelSerializer):
    
    name = serializers.CharField(source = 'first_name')
    phone = serializers.CharField(source = 'phone_number')
    
    
    class Meta:
        model= ApplicationUser
        field = ['name','email','phone','nid']
        
        
        