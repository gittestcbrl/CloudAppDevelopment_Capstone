from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    # maker or manufacturer of the car  eg: Toyota, Ford, Nissan
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)

    def __str__(self):
        return f'Car Name is {self.name} which {self.description}'


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    # specific car models  eg: Camry from Toyota
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    CAR_TYPE_CHOICES = [(SEDAN, SEDAN), (SUV, SUV), (WAGON, WAGON)]

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealerId = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    car_type = models.CharField(choices=CAR_TYPE_CHOICES, max_length=20)
    year = models.DateField()

    def __str__(self):
        return f'Dealer with ID {self.dealerId} has car of type {self.car_type} of make {self.make.name}'



# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
