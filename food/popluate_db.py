import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food.settings')

# Initialize Django
django.setup()

from app.models import Product  # Import your Product model
import pandas as pd

# Load your DataFrame from the pickle file
data = pd.read_pickle('C:\\Users\\SANIYA\\Downloads\\Rospl-Project\\food\\Pickle\\basic_dict.pkl')

# Iterate over each row in the DataFrame
for index in range(len(data['id'])):
    # Check if an entry with the same id already exists in the database
    existing_product = Product.objects.filter(id=data['id'][index]).first()
    if existing_product:
        # Update the existing entry with the new data
        existing_product.description = data['description'][index]
        existing_product.ProductId = data['ProductId'][index]
        existing_product.price = data['price'][index]
        existing_product.food_name = data['food_name'][index]
        existing_product.food_category = data['food_category'][index]
        existing_product.sub_category = data['sub_category'][index]
        existing_product.Image = data['Image'][index]
        existing_product.save()
    else:
        # Create a new Product object for the row
        Product.objects.create(
            id=data['id'][index],
            description=data['description'][index],
            ProductId=data['ProductId'][index],
            price=data['price'][index],
            food_name=data['food_name'][index],
            food_category=data['food_category'][index],
            sub_category=data['sub_category'][index],
            Image=data['Image'][index]
        )

# Print the food items added to the database
print("Food items added to the database:")
for product in Product.objects.all():
    print(f"- {product.food_name}")
