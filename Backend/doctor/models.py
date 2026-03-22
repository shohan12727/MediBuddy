from django.db import models
from django_resized import ResizedImageField
from hospital.models import Hospital


class Speciality(models.Model):
    name = models.CharField(null=False, blank=False)

    class Meta:
        verbose_name = "Speciality"

    def __str__(self):
        return self.name


class Doctor(models.Model):
    full_name = models.CharField(null=False, blank=False, max_length=100)
    gender = models.CharField(
        null=False,
        blank=False,
        max_length=15,
        choices=(("Male", "Male"), ("Female", "Female")),
    )
    profile_image = ResizedImageField(null=True, blank=True, upload_to="Doctor_Images/")
    degree = models.CharField(null=True, blank=True, max_length=150)
    speciality = models.ManyToManyField(Speciality)
    designation = models.CharField(null=True, blank=True, max_length=35)
    chamber_address = models.CharField(null=True, blank=True, max_length=100)
    hospital = models.ManyToManyField(Hospital)
    consulation_fee = models.IntegerField(null=False, blank=False, default=0)
    phone = models.CharField(null=True, blank=True, max_length=40)
    bmdc_registration_no = models.CharField(
        null=False, blank=False, max_length=20, default="Unregistered"
    )

    class Meta:
        verbose_name = "Doctor Info"

    def __str__(self):
        return f"{self.full_name} - {self.bmdc_registration_no}"


class DaySchedule(models.Model):
    DAYS = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Tuesday", "Tuesday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    ]

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="schedules"
    )
    day = models.CharField(max_length=10, choices=DAYS)
    available = models.CharField(default=False)

    class Meta:
        unique_together = ("doctor", "day")

    def __str__(self):
        return f"{self.doctor.full_name} - {self.get_day_display()}"


class TimeRange(models.Model):
    schedule = models.ForeignKey(
        DaySchedule, on_delete=models.CASCADE, related_name="time_ranges"
    )
    start = models.TimeField()
    end = models.TimeField()
    duration = models.PositiveIntegerField(default=30)

    class Meta:
        ordering = ["start"]

    def __str__(self):
        return f"{self.start} - {self.end} ({self.duration}m)"
