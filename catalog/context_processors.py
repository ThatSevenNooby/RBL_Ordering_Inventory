from .models import Category, Brand

def global_nav_data(request):
    return {
        'nav_categories': Category.objects.all(),
        'nav_brands': Brand.objects.all(),
    }