from django.shortcuts import render
from shop.models import ProductProxy, Category
from django.shortcuts import get_object_or_404


def main_page_view(request):
    featured_products = ProductProxy.objects.filter(is_new=True)[:4]
    return render(
        request,
        template_name="shop/main_view.html",
        context={"featured_products": featured_products},
    )


def wedding_dress_view(request):
    category = get_object_or_404(Category, slug="wedding_dress")
    products = ProductProxy.objects.filter(category=category)
    return render(request, "shop/product_list.html", {"products": products})


def evening_dress_view(request):
    category = get_object_or_404(Category, slug="evening_dress")
    products = ProductProxy.objects.filter(category=category)
    return render(request, "shop/product_list.html", {"products": products})


def product_list(request):
    products = ProductProxy.objects.all()
    return render(request, "shop/product_list.html", {"products": products})
