import json 
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from appointment.models import Appointment
from appointment.models import ApplicationUser
from .models import *
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from users.serializers import ApplicationUserSerializer
import requests
from django.db.models import Q

class DoctorListView(ListAPIView):
    
    queryset = Doctor.objects.all()
    serializer_class = DoctorListSerializer
    
    
class DoctorView(APIView):
    
    def get(self,request,doctor_id):
        doctor = Doctor.objects.get(id=doctor_id)
        serialized = DoctorSerializer(doctor, context={'request':request})
        
        
        return Response(serialized.data)
    
class DoctorProfileView(APIView):
    
    def get(self,request):
        username = request.user.username
        user = ApplicationUser.objects.get(
            Q(username = username) |
            Q(email = username)|
            Q(phone_number = username) |
            Q(nid = username)
        )        
        
        user_serialized = ApplicationUserSerializer(user).data
        
        if user.user_type == 'Doctor':
            
            doctor_data = Doctor.objects.get(id = user.user_id)
            doctor_serialized = DoctorSerializer(doctor_data, context = {'request':request}).data 
            
            user_serialized.update(doctor_serialized)
            
            return Response(user_serialized)
        
        else:
            return Response({'status':'error','message':'something is going wrong'})
    
    def post(self, request):
        
        full_name = request.POST.get('full_name')
        degrees = request.POST.get('degrees')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        chamber_address = request.POST.get('chamber_address') 
        speciality = request.POST.get('speciality')
        consultation_fee = request.POST.get('consultation_fee')
        profile_image = request.POST.get('profile_image')
        
        doctor_user = ApplicationUser.objects.get(username=request.user.username)
        doctor = Doctor.objects.get(id = doctor_user.user_id)
        doctor.full_name = full_name
        doctor.degrees = degrees
        doctor.phone = phone
        doctor.chamber_address = chamber_address
        doctor.consultation_fee = consultation_fee
        if profile_image:
            doctor.profile_image = profile_image
        doctor.save()
        
        
        doctor_user.first_name = full_name
        doctor_user.email = email 
        doctor_user.phone_number = phone
        doctor_user.save()
        
        return Response({'message':'success'})
    
class DoctorWeeklySchedules(APIView):
    
    def get(self,request):
        user = request.user.username
        doctor_id = get_object_or_404(ApplicationUser, username = user).user_id
        doctor = Doctor.objects.get(id=doctor_id)
        schedules = DaySchedule.objects.filter(doctor=doctor).prefetch_related('time_ranges')
        schedules_serialized = DayScheduleSerializer(schedules,many=True).data
        return Response(schedules_serialized)
    
        
        
        
            
        
        