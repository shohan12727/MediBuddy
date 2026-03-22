from rest_framework import serializers
from .models import *
# from doctor.models import Doctor 
# from doctor.serializers import DoctorListSerializers

class HospitalSerializer(serializers.ModelSerializer):
    
    hospital_id = serializers.IntegerField(source='id')
    location = serializers.CharField(source='address')
    total_doctors = serializers.SerializerMethodField()
    affiliated_doctors = serializers.SerializerMethodField()
    departments = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Hospital
        fields = ['hospital_id','name','hospital_type','division','district','thana','location','phone','email','website','departments','total_doctors','image','affiliatied_doctors','longitude','latitude']
        
        
    # def get_total_doctors(self, obj):
    #     return Doctor.objects.filter(hospitals=obj.id).count()
    
    # def get_affiliated_doctors(self, obj):
    #     doctors = Doctor.objects.filter(hospitals=obj.id)
    #     doctors_serialized = DoctorListSerializer(doctors, many=True).data
    #     return doctors_serialized