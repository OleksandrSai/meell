from django.db import models
from django.utils.text import slugify

from shop.utils import random_slug


class Category(models.Model):
    name = models.CharField(verbose_name="Назва категорії", max_length=250, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="children",
                               verbose_name="Батьківська категорія", null=True, blank=True)
    slug = models.SlugField(verbose_name="Лінк", max_length=250, unique=True, null=False, editable=True)
    meta_title = models.CharField(verbose_name="Meta Title", max_length=255, blank=True)
    meta_description = models.TextField(verbose_name="Meta Description", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        unique_together = ["slug", "parent"]
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        file_path = [self.name]
        k = self.parent
        while k is not None:
            file_path.append(k.name)
            k = k.parent
        return " > ".join(file_path[::-1])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name + random_slug())
            super(Category, self).save(*args, **kwargs)


class Brand(models.Model):
    name = models.CharField(verbose_name="Назва бренду", max_length=250, unique=True, db_index=True)
    slug = models.SlugField(verbose_name="Слаг", unique=True, blank=True)
    meta_title = models.CharField(verbose_name="Meta Title", max_length=255, blank=True)
    meta_description = models.TextField(verbose_name="Meta Description", blank=True)
    logo = models.ImageField(verbose_name="Логотип", upload_to='brands/logos/', blank=True, null=True)
    available = models.BooleanField(verbose_name="Наявність", default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name="Назва товару", max_length=250, db_index=True)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(verbose_name="Ціна")
    discount_percent = models.PositiveIntegerField(verbose_name="Знижка (%)", default=0)
    brand = models.ForeignKey(Brand, verbose_name="Бренд", on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, verbose_name="Категорія", on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(verbose_name="Основне зображення", upload_to='products/products/%Y/%m/%d')
    stock = models.PositiveIntegerField(verbose_name="В наявності", default=0)
    available = models.BooleanField(verbose_name="Наявність", default=True)
    is_new = models.BooleanField(verbose_name="Новинка", default=False)
    is_on_sale = models.BooleanField(verbose_name="Акційний товар", default=False)
    meta_title = models.CharField(verbose_name="Meta Title", max_length=255, blank=True)
    meta_description = models.TextField(verbose_name="Meta Description", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        """Ціна з урахування знижки"""
        if self.discount_percent > 0:
            discount = (self.price * self.discount_percent) / 100
            return self.price - discount
        return self.price

    def get_discounted_price_display(self):
        """Відображення ціни з урахуванням знижки для адмінки"""
        return f"{self.discounted_price:.2f} грн"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Товар"
    )
    image = models.ImageField(
        verbose_name="Зображення",
        upload_to='products/gallery/%Y/%m/%d'
    )

    is_main = models.BooleanField(
        verbose_name="Основне зображення",
        default=False
    )

    def __str__(self):
        return f"{self.product.name} ({self.id})"


class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):

    objects = ProductManager()

    class Meta:
        proxy = True
