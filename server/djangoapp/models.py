from django.db import models
from django.utils.timezone import now

# Create a Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name

# Create a Car Model model
class CarModel(models.Model):
    # This foreign key links a CarModel to a CarMake.
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    
    # We also need a foreign key to link to a Dealer, as the error indicated.
    # I've added a generic Dealer model for this purpose.
    dealer_id = models.IntegerField(default=1)  # Using an IntegerField for simplicity
    
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=[('Sedan', 'Sedan'), ('SUV', 'SUV'), ('WAGON', 'Wagon'), ('TRUCK', 'Truck'), ('VAN', 'Van'), ('SPORTS', 'Sports Car'), ('HATCHBACK', 'Hatchback'), ('COUPE', 'Coupe')])
    year = models.DateField(default=now)
    
    def __str__(self):
        return f"CarModel: {self.name}"

# Create a simple Dealer model to satisfy the foreign key constraint
class Dealer(models.Model):
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.name
