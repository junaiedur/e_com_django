from django.db import models
from django.urls import reverse
###########

# Create your models here
class Category(models.Model):

    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True) #blank= True aita debar mane hocce aita optional tai
    category_images = models.ImageField(upload_to='photos/categories', blank=True)

#amder jodi admin panela kono name r banan vul ase se ketre amra ai vabe chane korbo:
    class Meta:
        verbose_name = 'category' # akn a amr app ar name
        verbose_name_plural = 'categories' # akn a ami je nai solve kora dite chai seta

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

## gimini genarator for sub category
    def __str__(self):
        """
        String representation of the Category object.
        """
        return self.category_name

class SubCategory(models.Model):
    """
    Represents a subcategory linked to a main category.
    """
    # ForeignKey to link SubCategory to Category.
    # on_delete=models.CASCADE means if a Category is deleted, its SubCategories are also deleted.
    # related_name='subcategories' allows reverse lookup from Category to SubCategory (e.g., category.subcategories.all())
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    sub_category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    sub_category_images = models.ImageField(upload_to='photos/subcategories', blank=True)

    class Meta:
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'
        # Ensures that a subcategory name is unique within its parent category.
        # This means 'T-Shirt' can exist under 'Men' and 'Women', but not twice under 'Men'.
        unique_together = ('category', 'sub_category_name')

    def get_url(self):
        """
        Returns the URL for a specific subcategory.
        You will need to define a URL pattern in your urls.py that accepts both
        the category slug and the subcategory slug.
        Example URL pattern: path('<slug:category_slug>/<slug:subcategory_slug>/', views.products_by_subcategory, name='products_by_subcategory')
        """
        return reverse('products_by_subcategory', args=[self.category.slug, self.slug])

    def __str__(self):
        """
        String representation of the SubCategory object.
        """
        return f"{self.category.category_name} - {self.sub_category_name}"
## handle subategory under sub
class SubSubCategory(models.Model):
    """
    Represents a sub-subcategory linked to a subcategory.
    """
    # ForeignKey to link SubSubCategory to SubCategory.
    # on_delete=models.CASCADE means if a SubCategory is deleted, its SubSubCategories are also deleted.
    # related_name='subsubcategories' allows reverse lookup from SubCategory to SubSubCategory
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subsubcategories')
    sub_sub_category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    sub_sub_category_images = models.ImageField(upload_to='photos/subsubcategories', blank=True)

    class Meta:
        verbose_name = 'subsubcategory'
        verbose_name_plural = 'subsubcategories'
        # Ensures that a sub-subcategory name is unique within its parent subcategory.
        unique_together = ('sub_category', 'sub_sub_category_name')

    def get_url(self):
        """
        Returns the URL for a specific sub-subcategory.
        You will need to define a URL pattern in your urls.py that accepts
        category slug, subcategory slug, and sub-subcategory slug.
        Example URL pattern: path('<slug:category_slug>/<slug:subcategory_slug>/<slug:subsubcategory_slug>/', views.products_by_subsubcategory, name='products_by_subsubcategory')
        """
        return reverse('products_by_subsubcategory', args=[self.sub_category.category.slug, self.sub_category.slug, self.slug])

    def __str__(self):
        """
        String representation of the SubSubCategory object.
        """
        return f"{self.sub_category.category.category_name} - {self.sub_category.sub_category_name} - {self.sub_sub_category_name}"

