import os
import django
import requests
from django.core.files import File
from decimal import Decimal
import urllib.parse
import tempfile

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_shop.settings')
django.setup()

from products.models import Category, Product
from django.utils.text import slugify

def download_image(url, filename):
    """Download image from URL and save it to media folder"""
    try:
        # Add parameters to get a smaller image size
        parsed_url = list(urllib.parse.urlparse(url))
        params = {'w': '800', 'q': '80'}  # width=800px, quality=80%
        parsed_url[4] = urllib.parse.urlencode(params)
        url = urllib.parse.urlunparse(parsed_url)

        # Download the image
        response = requests.get(url)
        if response.status_code != 200:
            return None

        # Save the image to media folder
        media_path = os.path.join('media', filename)
        os.makedirs(os.path.dirname(media_path), exist_ok=True)
        
        with open(media_path, 'wb') as f:
            f.write(response.content)
        
        # Return Django File object
        return File(open(media_path, 'rb'))
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None

# Sample categories with their products
categories_data = {
    'Fruits': {
        'image': 'https://images.unsplash.com/photo-1610832958506-aa56368176cf',
        'products': [
            {
                'name': 'Fresh Apples',
                'description': 'Sweet and crispy red apples, perfect for snacking or baking.',
                'price': Decimal('199.00'),
                'stock': 100,
                'image': 'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce'
            },
            {
                'name': 'Bananas',
                'description': 'Ripe yellow bananas, rich in potassium and perfect for breakfast.',
                'price': Decimal('89.00'),
                'stock': 150,
                'image': 'https://images.unsplash.com/photo-1603833665858-e61d17a86224'
            },
            {
                'name': 'Oranges',
                'description': 'Juicy oranges packed with vitamin C.',
                'price': Decimal('149.00'),
                'stock': 75,
                'image': 'https://images.unsplash.com/photo-1582979512210-99b6a53386f9'
            }
        ]
    },
    'Vegetables': {
        'image': 'https://images.unsplash.com/photo-1597362925123-77861d3fbac7',
        'products': [
            {
                'name': 'Fresh Tomatoes',
                'description': 'Ripe, juicy tomatoes perfect for salads and cooking.',
                'price': Decimal('79.00'),
                'stock': 80,
                'image': 'https://images.unsplash.com/photo-1546094096-0df4bcaaa337'
            },
            {
                'name': 'Cucumbers',
                'description': 'Crisp, fresh cucumbers ideal for salads and sandwiches.',
                'price': Decimal('49.00'),
                'stock': 120,
                'image': 'https://images.unsplash.com/photo-1604977042946-1eecc30f269e'
            },
            {
                'name': 'Carrots',
                'description': 'Sweet and crunchy carrots, great for snacking or cooking.',
                'price': Decimal('59.00'),
                'stock': 90,
                'image': 'https://images.unsplash.com/photo-1447175008436-054170c2e979'
            }
        ]
    },
    'Dairy': {
        'image': 'https://images.unsplash.com/photo-1628088062854-d1870b4553da',
        'products': [
            {
                'name': 'Fresh Milk',
                'description': 'Farm-fresh whole milk, rich and creamy.',
                'price': Decimal('89.00'),
                'stock': 50,
                'image': 'https://images.unsplash.com/photo-1563636619-e9143da7973b'
            },
            {
                'name': 'Cheddar Cheese',
                'description': 'Aged cheddar cheese, perfect for sandwiches and cooking.',
                'price': Decimal('299.00'),
                'stock': 40,
                'image': 'https://images.unsplash.com/photo-1452195100486-9cc805987862'
            },
            {
                'name': 'Greek Yogurt',
                'description': 'Creamy Greek yogurt, high in protein.',
                'price': Decimal('129.00'),
                'stock': 60,
                'image': 'https://images.unsplash.com/photo-1488477181946-6428a0291777'
            }
        ]
    },
    'Bakery': {
        'image': 'https://images.unsplash.com/photo-1608198093002-ad4e005484ec',
        'products': [
            {
                'name': 'Whole Wheat Bread',
                'description': 'Freshly baked whole wheat bread, nutritious and delicious.',
                'price': Decimal('69.00'),
                'stock': 30,
                'image': 'https://images.unsplash.com/photo-1549740425-5e9ed4d8cd34'
            },
            {
                'name': 'Croissants',
                'description': 'Buttery, flaky croissants, perfect for breakfast.',
                'price': Decimal('89.00'),
                'stock': 25,
                'image': 'https://images.unsplash.com/photo-1555507036-ab1f4038808a'
            },
            {
                'name': 'Bagels',
                'description': 'Fresh bagels, great for sandwiches.',
                'price': Decimal('59.00'),
                'stock': 35,
                'image': 'https://images.unsplash.com/photo-1612203985729-70726954388c'
            }
        ]
    },
    'Beverages': {
        'image': 'https://images.unsplash.com/photo-1544252890-c3e4f8576e4c',
        'products': [
            {
                'name': 'Green Tea',
                'description': 'Premium green tea, rich in antioxidants.',
                'price': Decimal('249.00'),
                'stock': 45,
                'image': 'https://images.unsplash.com/photo-1563822249366-3e5d7d09c4a0'
            },
            {
                'name': 'Coffee Beans',
                'description': 'Freshly roasted coffee beans, perfect for your morning brew.',
                'price': Decimal('499.00'),
                'stock': 30,
                'image': 'https://images.unsplash.com/photo-1447933601403-0c6688de566e'
            },
            {
                'name': 'Orange Juice',
                'description': 'Freshly squeezed orange juice, packed with vitamin C.',
                'price': Decimal('159.00'),
                'stock': 40,
                'image': 'https://images.unsplash.com/photo-1621263764928-df1444c5e859'
            }
        ]
    }
}

def add_sample_data():
    # Create media directory if it doesn't exist
    if not os.path.exists('media'):
        os.makedirs('media')
        os.makedirs('media/categories')
        os.makedirs('media/products')

    # Clear existing data
    Category.objects.all().delete()
    Product.objects.all().delete()
    
    # Add categories and products
    for category_name, category_data in categories_data.items():
        print(f"\nProcessing category: {category_name}")
        
        # Download category image
        category_image_path = f"categories/{slugify(category_name)}.jpg"
        category_image = download_image(category_data['image'], category_image_path)
        
        # Create category
        category = Category.objects.create(
            name=category_name,
            slug=slugify(category_name),
            description=f'Fresh and high-quality {category_name.lower()} for your daily needs.'
        )
        
        # Save category image if downloaded successfully
        if category_image:
            category.image.save(category_image_path, category_image, save=True)
            print(f"Added image for category: {category_name}")
            category_image.close()
        
        # Add products for this category
        for product_data in category_data['products']:
            print(f"Processing product: {product_data['name']}")
            
            # Download product image
            product_image_path = f"products/{slugify(product_data['name'])}.jpg"
            product_image = download_image(product_data['image'], product_image_path)
            
            # Create product
            product = Product.objects.create(
                category=category,
                name=product_data['name'],
                slug=slugify(product_data['name']),
                description=product_data['description'],
                price=product_data['price'],
                stock=product_data['stock'],
                available=True
            )
            
            # Save product image if downloaded successfully
            if product_image:
                product.image.save(product_image_path, product_image, save=True)
                print(f"Added image for product: {product_data['name']}")
                product_image.close()
            
        print(f"Completed category: {category_name}")

if __name__ == '__main__':
    add_sample_data()
    print("\nSample data has been added successfully!") 