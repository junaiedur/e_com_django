# store/management/commands/import_products.py
import csv
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from store.models import Product # আপনার অ্যাপের নাম অনুযায়ী মডেল ইম্পোর্ট করুন
from category.models import Category # আপনার ক্যাটাগরি অ্যাপের মডেল
from django.db import IntegrityError 
import os # to check if image path exists

class Command(BaseCommand):
    help = 'Imports products from a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"Error: The specified CSV file does not exist at {csv_file_path}. Please provide a valid path."))
            return
        
        # Define media root based on your settings (assuming BASE_DIR is accessible or hardcode for command)
        # It's better to dynamically get MEDIA_ROOT from settings if possible, but for simplicity
        # let's assume images will be placed in a known path relative to manage.py
        # You should ensure your settings.py defines MEDIA_ROOT correctly
        # from django.conf import settings
        # media_root = settings.MEDIA_ROOT 
        
        # A simple relative path assumption for command line execution
        # Make sure your actual MEDIA_ROOT in settings.py points to where you place these images
        # Example: if MEDIA_ROOT is 'e_com/media', then image_full_path would be 'e_com/media/photos/products/...'
        # For this script, we just store 'photos/products/image_name.jpg' in the DB ImageField.
        # The actual files must exist in MEDIA_ROOT/photos/products.

        try:
            with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        # Find the category based on slug
                        category_slug = row['category_slug'].strip()
                        try:
                            category = Category.objects.get(slug=category_slug)
                        except Category.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f"Error: Category with slug '{category_slug}' does not exist for product '{row['product_name']}'. Please create this category first. Skipping product."))
                            continue 

                        # Convert boolean string to actual boolean
                        is_available = row['is_available'].strip().lower() == 'true'

                        # Construct image path for ImageField
                        # The ImageField only stores the relative path from MEDIA_ROOT
                        image_db_path = f"photos/products/{row['image'].strip()}"

                        Product.objects.create(
                            product_name=row['product_name'].strip(),
                            slug=row['slug'].strip(),
                            description=row['description'].strip(),
                            category=category,
                            price=int(row['price']),
                            image=image_db_path, 
                            stock=int(row['stock']),
                            is_available=is_available,
                            # created_date and modified_date will be auto-populated by Django
                        )
                        self.stdout.write(self.style.SUCCESS(f"Successfully added product: {row['product_name']}"))
                    except IntegrityError:
                        self.stdout.write(self.style.WARNING(f"Warning: Product '{row['product_name']}' with slug '{row['slug']}' already exists (unique constraint violation). Skipping."))
                    except KeyError as e:
                        self.stdout.write(self.style.ERROR(f"Error: Missing column '{e}' in CSV row for product '{row.get('product_name', 'N/A')}'. Please check CSV headers. Skipping."))
                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(f"Error: Data conversion issue for product '{row.get('product_name', 'N/A')}'. Ensure price/stock are numbers and is_available is True/False. Error: {e}. Skipping."))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"An unexpected error occurred for row (Product: {row.get('product_name', 'N/A')}): {e}. Skipping."))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Error: CSV file not found at {csv_file_path}. Please provide the correct path."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred while opening/reading the CSV file: {e}"))