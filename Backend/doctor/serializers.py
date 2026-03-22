from rest_framework import serializers
from .models import *
from appointment.models import Appointment, AppointmentDocuments, AppointmentDocumentsSummary

from .models import *

class DoctorSerializer(serializers.ModelSerializer):
    
    doctor_id = serializers.IntegerField(source = 'id')
    speciality = serializers.StringRelatedField(many=True)
    hospitals = serializers.StringRelatedField(many=True)
    schedule = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Doctor
        fields = ['doctor_id','full_name','gender','profile_image','degrees','speciality','designation','chamber_address','hospitals','schedule','consultation_fee','phone','bmdc_registration_no']
        
        
    def get_schedule(self,obj):
        schedules = obj.schedules.all()
        
        result = []
        
        for schedule in schedules:
            if not schedule.available:
                continue
            
            ranges = schedule.time_ranges.all()
            
            
            if not ranges.exists():
                continue
            
            result.append({
                "day": schedule.day,
                "time_ranges": [
                    {
                        "start": tr.start.strftime("%I:%M %p"),  # AM/PM format
                        "end": tr.end.strftime("%I:%M %p"),
                        "duration": tr.duration,
                    }
                    for tr in ranges 
                ]
            })
        return result        
    
class DoctorListSerializer(serializers.ModelSerializer):
    
    doctor_id = serializers.IntegerField(source='id')
    speciality = serializers.StringRelatedField(many=True)
    hospitals = serializers.StringRelatedField(many=True)
    schedule = serializers.SerializerMethodField()
    
    
    class Meta:
        model : Doctor
        fields = ['doctor_id','full_name','profile_image','degrees','speciality','designation','chamber_address','hospitals','schedule','consultation_fee']
        
        
        
    def get_schedule(self,obj):
        return {
                "days": ["Sat", "Sun", "Mon", "Tue"],
                "start_time": "6:00 PM",
                "end_time": "9:00 PM"
            
        }
        
class TimeRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRange
        fields = ['id','start','end','duration'] 
        
               
# class         
        
            