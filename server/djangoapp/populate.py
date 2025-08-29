from .models import CarMake, CarModel, Dealer
from datetime import date

def initiate():
    """
    Initializes the database with pre-defined CarMake and CarModel objects.
    This function is designed to be idempotent; it will not add duplicate data if the tables are already populated.
    """
    # Check if a dealer exists, and create one if not.
    if Dealer.objects.count() == 0:
        print("Creating a sample dealer...")
        Dealer.objects.create(name='Your Local Dealership', city='Anytown', state='CA', zip_code='12345')
        print("Dealer created.")

    # Check if the database has already been populated with car makes
    if CarMake.objects.count() == 0:
        print("Populating CarMakes...")
        
        # List of car makes to be created
        car_makes_data = [
            {'name': 'Nissan', 'description': 'The best cars on the planet'},
            {'name': 'Mercedes-Benz', 'description': 'The best or nothing'},
            {'name': 'Ford', 'description': 'Built Tough'},
            {'name': 'Honda', 'description': 'The Power of Dreams'},
            {'name': 'Chevrolet', 'description': 'Find New Roads'}
        ]

        # Create CarMake objects from the list
        for data in car_makes_data:
            CarMake.objects.create(name=data['name'], description=data['description'])
        
        print("CarMakes populated.")
    
    # Check if the database has already been populated with car models
    if CarModel.objects.count() == 0:
        print("Populating CarModels...")
        
        # Retrieve the single dealer created above
        dealer = Dealer.objects.first()
        if not dealer:
            print("No dealer found. Please ensure a dealer is created before populating car models.")
            return

        # Create CarModel objects and link them to the appropriate CarMake and the Dealer
        CarModel.objects.create(name='Pathfinder', car_make=CarMake.objects.get(name='Nissan'), dealer_id=dealer.id, type='SUV', year=date(2019, 1, 1))
        CarModel.objects.create(name='Titan', car_make=CarMake.objects.get(name='Nissan'), dealer_id=dealer.id, type='TRUCK', year=date(2022, 1, 1))
        CarModel.objects.create(name='Frontier', car_make=CarMake.objects.get(name='Nissan'), dealer_id=dealer.id, type='TRUCK', year=date(2022, 1, 1))

        CarModel.objects.create(name='C-Class', car_make=CarMake.objects.get(name='Mercedes-Benz'), dealer_id=dealer.id, type='Sedan', year=date(2023, 1, 1))
        CarModel.objects.create(name='E-Class', car_make=CarMake.objects.get(name='Mercedes-Benz'), dealer_id=dealer.id, type='Sedan', year=date(2022, 1, 1))
        CarModel.objects.create(name='GLE', car_make=CarMake.objects.get(name='Mercedes-Benz'), dealer_id=dealer.id, type='SUV', year=date(2023, 1, 1))
        
        CarModel.objects.create(name='F-150', car_make=CarMake.objects.get(name='Ford'), dealer_id=dealer.id, type='TRUCK', year=date(2021, 1, 1))
        CarModel.objects.create(name='Fusion', car_make=CarMake.objects.get(name='Ford'), dealer_id=dealer.id, type='Sedan', year=date(2020, 1, 1))
        CarModel.objects.create(name='Explorer', car_make=CarMake.objects.get(name='Ford'), dealer_id=dealer.id, type='SUV', year=date(2022, 1, 1))
        
        CarModel.objects.create(name='Accord', car_make=CarMake.objects.get(name='Honda'), dealer_id=dealer.id, type='Sedan', year=date(2023, 1, 1))
        CarModel.objects.create(name='CR-V', car_make=CarMake.objects.get(name='Honda'), dealer_id=dealer.id, type='SUV', year=date(2024, 1, 1))
        
        CarModel.objects.create(name='Silverado', car_make=CarMake.objects.get(name='Chevrolet'), dealer_id=dealer.id, type='TRUCK', year=date(2023, 1, 1))
        CarModel.objects.create(name='Malibu', car_make=CarMake.objects.get(name='Chevrolet'), dealer_id=dealer.id, type='Sedan', year=date(2022, 1, 1))
        
        print("CarModels populated.")
    
    print("Database population complete.")
