from django.contrib import admin
from . models import Category ,SubCategory, SubSubCategory


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug', 'description')

# gimini genarator for sub category:

class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('sub_category_name',)}
    list_display = ('sub_category_name', 'category', 'slug')
    list_filter = ('category',) # Allows filtering subcategories by their parent category

class SubSubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('sub_sub_category_name',)}
    list_display = ('sub_sub_category_name', 'sub_category', 'slug')
    list_filter = ('sub_category',)
# handaling subcategory under subcategory:

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(SubSubCategory, SubSubCategoryAdmin)

