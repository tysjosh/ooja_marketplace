from django.contrib.gis.db import models # GeoDjango Model API
from user.models import CustomUser
from django.utils.translation import gettext_lazy as _



class StoreCategory(models.Model):
    name = models.CharField(_('Store Category Name'), max_length=50)

    def __str__(self):
        return self.name

class Store(models.Model):
    """
    Store details table
    """
    web_id = models.CharField(max_length=50,unique=True,
        verbose_name=_("store website ID"),
        help_text=_("format: required, unique"),
    )
    slug = models.SlugField(max_length=255, verbose_name=_("store safe URL"),
        help_text=_(
            "format: required, letters, numbers, underscores or hyphens"
        ),
    )
    name = models.CharField(_('Store Name'), max_length=50, unique=True)
    category = models.ManyToManyField(StoreCategory)
    description = models.CharField(_('Store Description'), max_length=500)
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    street_1 = models.CharField(max_length=200)
    street_2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    location = models.PointField(_('Store location'), srid=4326, null=True)

    class Meta:
        verbose_name = _("Store")
        verbose_name_plural = _("Stores")

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    """
    Product details table
    """
    web_id = models.CharField(max_length=50, unique=True,
        verbose_name=_("product website ID"),
        help_text=_("format: required, unique"),
    )
    slug = models.SlugField(max_length=255, verbose_name=_("product safe URL"),
        help_text=_(
            "format: required, letters, numbers, underscores or hyphens"
        ),
    )
    name = models.CharField(_('Product Name'), max_length=50, unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(_('Product Description'), max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

class ProductType(models.Model):
    name = models.CharField(_('Product Type Name'), max_length=50)

    def __str__(self):
        return self.name

class ProductInventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    retail_price = models.DecimalField(decimal_places=2, max_digits=10)
    sale_price = models.DecimalField(decimal_places=2, max_digits=10)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class ProductImage(models.Model):

    def get_image_filename(self, instance, filename):
        return '{0}/{1}/{2}'.format(instance.product.store.user, instance.product.name, filename)
    
    product = models.ForeignKey(ProductInventory, null=True, on_delete=models.CASCADE)
    file = models.ImageField(_('Image'), upload_to=get_image_filename)
    title = models.CharField(max_length=128)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    product_type = models.ManyToManyField(ProductType)
    name = models.CharField(_('Product Attribute Name'), max_length=50)
    description = models.CharField(_('Product Attribute Description'), max_length=500)

    def __str__(self):
        return '%s %s' % (self.product_type, self.name)

class AttributeValue(models.Model):
    product = models.ManyToManyField(ProductInventory)
    product_attribute = models.ForeignKey(ProductAttribute, null=True, on_delete=models.CASCADE)
    value = models.CharField(_('Attribute Value'), max_length=50)

    def __str__(self):
        return '%s %s %s' % (self.product, self.product_attribute, self.value)

class Stock(models.Model):
    product = models.OneToOneField(ProductInventory, null=True, blank=True, on_delete=models.CASCADE)
    units_left = models.IntegerField(_('Number of Products in stock'), default=0)
    units_sold = models.IntegerField(_('Number of Products in sold'), default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s %s' % (self.product, self.units_left, self.units_sold)

class Coupon(models.Model):
    name = models.CharField(_('Coupon Name'), max_length=50)
    coupon_code = models.CharField(_('Coupon Code'), max_length=50)

    def __str__(self):
        return '%s %s' % (self.name, self.coupon_code)

class PromoType(models.Model):
    name = models.CharField(_('Promo Type Name'), max_length=50)

    def __str__(self):
        return self.name

class Promotion(models.Model):
    name = models.CharField(_('Promotion Name'), max_length=50)
    description = models.CharField(_('Promotion Name'), max_length=500)
    promo_product = models.ManyToManyField(ProductInventory)
    promo_reduction = models.DecimalField(decimal_places=2, max_digits=10)
    promo_type = models.ForeignKey(PromoType, null=True, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, null=True, on_delete=models.CASCADE)
    promo_start = models.DateTimeField()
    promo_end = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    is_scheduled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    class Ratings(models.IntegerChoices):
        BAD = 1
        OKAY = 2
        GOOD = 3
        VERY_GOOD = 4
        EXCELLENT = 5

    product = models.ForeignKey(ProductInventory, null=True, on_delete=models.CASCADE)
    comment = models.CharField(_('Comment'), max_length=500)
    rating = models.IntegerField(choices=Ratings.choices, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s %s' % (self.product, self.comment, self.rating)