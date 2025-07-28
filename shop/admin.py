from django.contrib import admin

from .models import Brand, Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "slug")
    ordering = ("name",)

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "brand",
        "price",
        "discount_percent",
        "stock",
        "available",
        "is_new",
        "is_on_sale",
        "created_at",
        "updated_at",
    )
    list_filter = ("brand", "available", "created_at", "updated_at")
    ordering = ("name",)

    def get_prepopulated_field(self, request, obj=None):
        return {"slug": ("name",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "available",
        "created_at",
        "updated_at",
    )
    list_filter = ("name", "available", "created_at", "updated_at")
    ordering = ("name",)

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": ("name",)}
