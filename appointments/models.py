from django.db import models
from accounts.models import User

class Appointment(models.Model):
    """
    Appointment booking model for grooming and vaccination
    """
    SERVICE_TYPES = (
        ('Grooming', 'Grooming'),
        ('Vaccination', 'Vaccination'),
        ('Checkup', 'General Checkup'),
        ('Visit', 'Pet Visit'),
        ('Adoption', 'Pet Adoption'),
    )
    
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPES)
    pet_name = models.CharField(max_length=200)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'appointments'
        ordering = ['-appointment_date', '-appointment_time']
        indexes = [
            models.Index(fields=['appointment_date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.service_type} - {self.pet_name} on {self.appointment_date}"
    
    @property
    def status_badge_class(self):
        """Return Bootstrap badge class based on status"""
        status_classes = {
            'Pending': 'warning',
            'Approved': 'info',
            'Completed': 'success',
            'Cancelled': 'danger',
        }
        return status_classes.get(self.status, 'secondary')
