# generate_products_csv.py
import csv
import random
from django.utils.text import slugify

# Define the categories and their slugs
categories = {
    'জামা': 'jama',
    'পেন্ট': 'pant',
    'জুতা': 'juta',
    'গেঞ্জি': 'genji',
    'শার্ট': 'shirt',
    'টুপি': 'tupi',
}

# Base product names for variety
base_names = [
    "প্রিমিয়াম কটন", "স্টাইলিশ", "স্পোর্টস", "গ্রাফিক", "ফরমাল", "ফ্যাশনেবল",
    "দৈনন্দিন ব্যবহারের", "ক্যাজুয়াল", "ট্র্যাকিং", "সাদা", "স্লিম ফিট", "উলের",
    "ভিন্টেজ", "আধুনিক", "আরামদায়ক", "টেকসই", "নরম", "শ্বাসপ্রশ্বাসযোগ্য", "মার্জিত", "এলিগেন্ট",
    "ডিজাইনার", "উন্নত মানের", "আউটডোর", "কম্প্যাক্ট", "লাইটওয়েট"
]

products_data = []
product_counter = 1

# Generate 1000 unique products
while len(products_data) < 1000:
    category_name = random.choice(list(categories.keys()))
    category_slug = categories[category_name]
    
    base_name = random.choice(base_names)
    product_name_suffix = f"-{product_counter}"
    
    product_name = f"{base_name} {category_name}{product_name_suffix}"
    product_slug = slugify(product_name)
    
    # Ensure slug is unique (though with product_counter it should be unique)
    existing_slugs = {p['slug'] for p in products_data}
    if product_slug in existing_slugs:
        product_counter += 1
        continue # Retry with new counter for uniqueness

    description = f"{product_name} এর বিবরণ: উচ্চ মানের উপাদান দিয়ে তৈরি, এটি প্রতিদিনের ব্যবহারের জন্য আরামদায়ক এবং স্টাইলিশ।"
    
    price = random.randint(400, 3000) if category_name not in ['জুতা'] else random.randint(1500, 5000)
    stock = random.randint(10, 300)
    is_available = random.choice([True, True, True, False]) # More likely to be available

    image_name = f"{product_slug}.jpg" # Or you could use a generic product_{product_counter}.jpg

    products_data.append({
        'product_name': product_name,
        'slug': product_slug,
        'description': description,
        'category_slug': category_slug,
        'price': price,
        'image': image_name,
        'stock': stock,
        'is_available': is_available
    })
    product_counter += 1

# Write to CSV
csv_file_path = 'products_1000.csv'
fieldnames = ['product_name', 'slug', 'description', 'category_slug', 'price', 'image', 'stock', 'is_available']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(products_data)

print(f"Generated {len(products_data)} products and saved to {csv_file_path}")