from django.db import models
from django.utils import timezone



class FitnessClass(models.Model):
    name = models.CharField(max_length=100,unique=True)
    start_time = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField(null=True, blank=True)  # Allow initially blank

    def save(self, *args, **kwargs):
        # Set available_slots to total_slots only when the class is created
        if self._state.adding and self.available_slots is None:
            self.available_slots = self.total_slots
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class.name}"
