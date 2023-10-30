# Additional context processor for loading all listing categories

def categories(request):
    from .models import Category
    categories = Category.objects.all()
    return {'categories': categories}