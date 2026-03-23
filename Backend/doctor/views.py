import json 
from django.shortcuts import get_list_or_404, render
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
        
        