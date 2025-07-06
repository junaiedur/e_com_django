from .models import Category, SubCategory, SubSubCategory


# def menu_links(request):
#     links = Category.objects.all()
#     return dict(links=links).prefetch_related('subcategories')
#     return dict(links=links)

def menu_links(request):
    # Fetch top-level categories and prefetch related subcategories
    links = Category.objects.prefetch_related('subcategories').all()
    #nicher ai line ta bad o jaite pare
    links = Category.objects.all().prefetch_related(
        'subcategories__subsubcategories'
    )
    return dict(links=links)

