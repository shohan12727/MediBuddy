from django.db import models

from doctor.models import Doctor
from users.models import ApplicationUser

# Create your models here.


class Appointment(models.Model):
    APPOINTMENT_TYPES_CHOICES = [
        ("regular_checkup", "Regular-Checkup"),
        ("consultation", "consultation"),
        ("emergency", "emergency"),
        ("follow_up", "follow_up"),
    ]

    STATUS_CHOICES = [
        ("upcoming", "upcoming"),
        ("completed", "completed"),
        ("cancelled", "cancelled"),
        ("pending", "pending"),
    ]

    GENDER_CHOICES = [("male", "male"), ("female", "female"), ("other", "other")]

    full_name = models.CharField(null=True, blank=True, max_length=40, default="")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    gender = models.CharField(
        null=True, blank=True, max_length=10, choices=GENDER_CHOICES
    )
    age = models.SmallIntegerField(null=False, blank=False, default=0)
    appointment_type = models.CharField(
        choices=APPOINTMENT_TYPES_CHOICES, null=False, blank=False, max_length=20
    )

    reason_for_visit = models.TextField(null=True, blank=True, default="")
    
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(ApplicationUser, null=True,blank=True, on_delete=models.CASCADE)
    
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    status = models.CharField(null=False,blank=False, max_length=11, default='Pending')
    
    class Meta: 
        unique_together = ('doctor','date','start_time')
        
        
    def __str__(self):
        return f"{self.doctor.full_name} - {self.date} {self.start_time}"    


class AppointmentDocuments(models.Model):
    
    appointment = models.ForeignKey(Appointment, null= False, blank=False, on_delete=models.CASCADE)
    document = models.FileField(null=False,blank=False,upload_to='Appointment Files/')
    
    
    class Meta:
        verbose_name = 'Appointment Documents'
        
    def __str__(self):
        return str(self.pk)
    
class AppointmentDocumentsSummary(models.Model):
    appointment_document = models.ForeignKey(AppointmentDocuments,null=False,blank=False,on_delete=models.CASCADE)
    summary = models.TextField(null=True,blank=True)
    
    
    class Meta:
        verbose_name = 'Appointment Document Summary'
        
        
    def __str___(self):
        return str(self.pk) 
    
class Prescription(models.Model):
    
    appointment = models.ForeignKey(Appointment, null=False,blank=False, on_delete=models.CASCADE)
    diagnosis = models.TextField(null=True,blank=True,default='')
    tests = models.TextField(null=True,blank=True,default='')
    additional_instructions = models.TextField(null=True,blank=True, default='')
    medications = models.JSONField(null=True,blank=True, default=[])
    
    
    class Meta:
        verbose_name = 'Prescription'
        
        
    def __str__(self):
        return str(self.pk)                        