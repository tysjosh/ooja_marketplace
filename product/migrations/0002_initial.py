# Generated by Django 4.0.4 on 2022-08-29 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='stock',
            name='product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productinventory'),
        ),
        migrations.AddField(
            model_name='review',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productinventory'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='coupon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.coupon'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='promo_product',
            field=models.ManyToManyField(to='product.productinventory'),
        ),
        migrations.AddField(
            model_name='promotion',
            name='promo_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.promotype'),
        ),
        migrations.AddField(
            model_name='productinventory',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
        migrations.AddField(
            model_name='productinventory',
            name='product_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.producttype'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productinventory'),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='product_type',
            field=models.ManyToManyField(to='product.producttype'),
        ),
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.store'),
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='product',
            field=models.ManyToManyField(to='product.productinventory'),
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='product_attribute',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productattribute'),
        ),
    ]
