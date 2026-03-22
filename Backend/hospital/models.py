from django.db import models
from django_resized import ResizedImageField

# Create your models here.


class Department(models.Model):
    name = models.CharField(null=False, blank=False, default="Untitled Department")

    class Meta:
        verbose_name = "Hospital Department"

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField(
        null=False, blank=False, max_length=100, default="Untitled Hospital"
    )
    hospital_type = models.CharField(
        max_length=20,
        choices=(
            ("Not Set", "Not Set"),
            ("Private", "Private"),
            ("Public", "Public"),
        ),
        default="Not set",
    )

    division = models.CharField(null=True, blank=True, max_length=40)
    district = models.CharField(null=True, blank=True, max_length=40)
    thana = models.CharField(null=True, blank=True, max_length=40)
    address = models.CharField(null=True, blank=True, max_length=40)
    phone = models.CharField(null=True, blank=True, max_length=40)
    email = models.CharField(null=True, blank=True, max_length=40)
    website = models.CharField(null=True, blank=True, max_length=40)
    department = models.ManyToManyField(Department, blank=True)
    image = ResizedImageField(null=True, blank=True, upload_to="Hospital_Images/")
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Hospital"

    def __str__(self):
        return self.name
