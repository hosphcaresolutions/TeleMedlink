from django.db import models
from users.models import Patients ,Doctors
from django.conf import settings
from django.utils.timezone import now
from django.db.models.signals import pre_save
#from doctors.models import DoctorProfile
from django.dispatch import receiver
#from django.contrib.gis.db import models as gis_models
from django.conf import settings
# emmergency alert
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from users.models import Patients  # Rename to avoid conflict


User = get_user_model()

class Time(models.Model):
    time = models.CharField(max_length=10)
    class Meta:
        verbose_name = "Time"
        verbose_name_plural = "Times"
    def __str__(self):
        return self.time
    
class Status(models.Model):
    status =  models.CharField(max_length=20) 
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"
    def __str__(self):
        return self.status

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, )
    summary = models.TextField()
    comment = models.TextField(blank=True, null=True)
    #description = models.TextField()
    start_date = models.DateField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, )
    time = models.ForeignKey(Time, on_delete=models.CASCADE, default=1)
    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"
    def __str__(self):
        return self.summary


# Emergency Alert system
class EmergencyAlert(models.Model):
    patient = models.ForeignKey(
        Patients,  # Use the existing Patients model from users
        on_delete=models.CASCADE,
        related_name='emergency_alerts'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Emergency alert for {self.patient.user.get_full_name()} at {self.timestamp}"
    
   

# Report
class Report(models.Model):
    patient = models.ForeignKey(
        Patients, on_delete=models.CASCADE, related_name="reports",
        null=True, blank=True  # Temporarily allow null for migration
    )
    doctor = models.ForeignKey(
        Doctors, on_delete=models.SET_NULL, null=True, blank=True, related_name="reports"
    )
    title = models.CharField(max_length=255)
    #description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=255)
    content = models.TextField()

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report: {self.title} - {self.patient.user.get_full_name() if self.patient else 'Unknown'} ({self.created_at.strftime('%Y-%m-%d')})"


# Auto-assign patient before saving the report
@receiver(pre_save, sender=Report)
def assign_patient(sender, instance, **kwargs):
    if instance.patient is None and instance.user:  # If no patient is assigned
        try:
            instance.patient = Patients.objects.get(user=instance.user)  # Assign patient
        except Patients.DoesNotExist:
            pass  # If user is not a patient, do nothing

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


# location
class Location(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - ({self.latitude}, {self.longitude})"
    
