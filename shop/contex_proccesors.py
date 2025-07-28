from .models import Category


def categories(request):
    main_categories = Category.objects.all().filter(parent=None)
    return {"categories": main_categories}
