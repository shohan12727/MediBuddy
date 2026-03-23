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
        
               
class DayScheduleSerializer(serializers.ModelSerializer):
    time_ranges = TimeRangeSerializer(many=True)
    
    class Meta:
        model: DaySchedule
        fields = ['id','day','available','time_ranges']
        
        
        
        def create(self, validated_data):
            time_ranges_data = validated_data.pop('time_ranges',[])
            schedule = DaySchedule.objects.create(**validated_data)
            for tr_data in time_ranges_data:
                TimeRange.objects.create(schedule=schedule,**tr_data)
            return schedule
        
        def update(self,instance,validated_data):
            time_ranges_data = validated_data.pop('time_ranges',[])
            
            instance.available = validated_data.get('available', instance.available)
            instance.save()
            
            instance.time_ranges.all().delete()
            for tr_data in time_ranges_data:
                TimeRange.objects.create(schedule=instance, **tr_data)
                
            return instance
        
class DoctorAppointmentSerializer(serializers.ModelSerializer):
    
    patient_name = serializers.CharField(scource = 'full_name')
    type = serializers.CharField(source = 'get_appointment_type_display') 
    
    class Meta:
        model = Appointment
        fields = ['id','patient_name','start_time','end_time','date','status','type']
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)    
        
        if rep.get('start_time'):
            rep["start_time"] = instance.start_time.strftime("%I:%M %p")
            
        if rep.get("end_time"):
            rep["end_time"] = instance.end_time.strftime("%I:%M %p")    
            
        return rep     
    
class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='full_name')
    type = serializers.CharField(source='get_appointment_type_display')
    doctor_name = serializers.CharField(source='doctor.full_name')    
    reason = serializers.CharField(source= 'reason_for_visit')
    documents = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Appointment
        fields = ['id','patient_name','phone_number','email','type','date','start_time','end_time','status','reason','doctor_name','documents']
        
    def get_documents(self,obj):
        request = self.context.get('request')
        
        self.documents = AppointmentDocuments.objects.filter(appointment=obj)
        
        data = []
        for doc in documents:
            try:
                summary = AppointmentDocumentsSummary.objects.get(appointment_document=doc)
            except:
                summary = None

            if doc.document:
                file_url = doc.document.url
                # convert to absolute URL
                absolute_url = request.build_absolute_uri(file_url) if request else file_url
            else:
                absolute_url = None
            data.append({
                'id': doc.id,
                'file': absolute_url,
                'summary': summary.summary if summary else ''
            })

        return data
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # Convert HH:MM to 12-hour AM/PM
        if rep.get("start_time"):
            rep["start_time"] = instance.start_time.strftime("%I:%M %p")

        if rep.get("end_time"):
            rep["end_time"] = instance.end_time.strftime("%I:%M %p")

        return rep
            
class AppointmentSerializerSmall(serializers.ModelSerializer):
    gender = serializers.CharField(source = 'get_gender_display')
    doctor_name = serializers.CharField(source = 'doctor.full_name')
    speciality = serializers.StringRelatedField(source = 'doctor.speciality', many= True)
    hospital_name = serializers.StringRelatedField(source = 'doctor.hospitals', many=True)
    
    class Meta:
        model = Appointment
        fields = ['id','full_name','age','gender','doctor_name','speciality','hospital_name']            