from .models import Category, Brand

def global_nav_data(request):
    # This fetches all categories and brands and makes them 
    # available to EVERY html file under these dictionary keys.
    return {
        'nav_categories': Category.objects.all(),
        'nav_brands': Brand.objects.all(),
    }