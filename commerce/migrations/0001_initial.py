# Generated by Django 3.2.7 on 2021-09-27 17:39

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('work_address', models.BooleanField(blank=True, null=True, verbose_name='work address')),
                ('address1', models.CharField(max_length=255, verbose_name='address1')),
                ('address2', models.CharField(blank=True, max_length=255, null=True, verbose_name='address2')),
                ('phone', models.CharField(max_length=255, verbose_name='phone')),
            ],
            options={
                'verbose_name': 'address',
                'verbose_name_plural': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('image', models.ImageField(upload_to='category/', verbose_name='image')),
                ('is_active', models.BooleanField(verbose_name='is active')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='commerce.category', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='city')),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('item_qty', models.IntegerField(verbose_name='item_qty')),
                ('ordered', models.BooleanField(verbose_name='ordered')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
            },
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            options={
                'verbose_name': 'label',
                'verbose_name_plural': 'labels',
            },
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merchant', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'merchant',
                'verbose_name_plural': 'merchants',
            },
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(choices=[('NEW', 'NEW'), ('PROCESSING', 'PROCESSING'), ('SHIPPED', 'SHIPPED'), ('COMPLETED', 'COMPLETED'), ('REFUNDED', 'REFUNDED')], max_length=255, verbose_name='title')),
                ('is_default', models.BooleanField(verbose_name='is default')),
            ],
            options={
                'verbose_name': 'order status',
                'verbose_name_plural': 'order status',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.SlugField(default=uuid.uuid4, unique=True, verbose_name='slug')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='description')),
                ('weight', models.FloatField(blank=True, null=True, verbose_name='weight')),
                ('width', models.FloatField(blank=True, null=True, verbose_name='width')),
                ('height', models.FloatField(blank=True, null=True, verbose_name='height')),
                ('length', models.FloatField(blank=True, null=True, verbose_name='length')),
                ('lowest', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='lowest')),
                ('lowest_discounted', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='lowest_discounted')),
                ('is_featured', models.BooleanField(verbose_name='is featured')),
                ('is_active', models.BooleanField(verbose_name='is active')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='commerce.category', verbose_name='category')),
                ('label', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='commerce.label', verbose_name='label')),
                ('merchant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='commerce.merchant', verbose_name='merchant')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
        ),
        migrations.CreateModel(
            name='Promo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='name')),
                ('code', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='code')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('is_active', models.BooleanField(blank=True, null=True, verbose_name='is active')),
                ('type', models.CharField(blank=True, choices=[('percentage', 'percentage'), ('fixed', 'fixed'), ('free_shipping', 'free_shipping')], max_length=255, null=True, verbose_name='type')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='amount')),
                ('active_from', models.DateTimeField(blank=True, null=True, verbose_name='active from')),
                ('active_till', models.DateTimeField(blank=True, null=True, verbose_name='active till')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'promo',
                'verbose_name_plural': 'promos',
            },
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('image', models.ImageField(upload_to='vendor/', verbose_name='image')),
                ('slug', models.SlugField(verbose_name='slug')),
            ],
            options={
                'verbose_name': 'vendor',
                'verbose_name_plural': 'vendors',
            },
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(choices=[('Color', 'Color'), ('Size', 'Size'), ('Storage', 'Storage'), ('Memory', 'Memory'), ('Number of pieces', 'Number of pieces'), ('Basic', 'Basic')], max_length=255, verbose_name='name')),
                ('value', models.CharField(max_length=255, verbose_name='value')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='commerce.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'variant',
                'verbose_name_plural': 'variants',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(choices=[('Color', 'Color'), ('Size', 'Size'), ('Storage', 'Storage'), ('Memory', 'Memory'), ('Number of pieces', 'Number of pieces'), ('Basic', 'Basic')], max_length=255, verbose_name='name')),
                ('value', models.CharField(max_length=255, verbose_name='value')),
                ('attachment', models.ImageField(upload_to='variant/', verbose_name='attachment')),
                ('barcode', models.CharField(blank=True, max_length=255, null=True, verbose_name='barcode')),
                ('merchant_barcode', models.CharField(blank=True, max_length=255, null=True, verbose_name='merchant barcode')),
                ('qty', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='qty')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='cost')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('discounted_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='discounted price')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='commerce.variant', verbose_name='variant')),
            ],
            options={
                'verbose_name': 'property',
                'verbose_name_plural': 'properties',
                'unique_together': {('variant', 'value')},
            },
        ),
        migrations.CreateModel(
            name='PromoUsage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('promo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commerce.promo')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='product/', verbose_name='image')),
                ('alt_text', models.CharField(blank=True, max_length=255, null=True, verbose_name='alt text')),
                ('is_default_image', models.BooleanField(verbose_name='is default image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='commerce.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'product image',
                'verbose_name_plural': 'product images',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='commerce.vendor', verbose_name='vendor'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('total', models.DecimalField(blank=True, decimal_places=0, max_digits=1000, null=True, verbose_name='total')),
                ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='note')),
                ('ref_code', models.CharField(max_length=255, verbose_name='ref code')),
                ('ordered', models.BooleanField(verbose_name='ordered')),
                ('shipping', models.DecimalField(blank=True, decimal_places=0, max_digits=1000, null=True, verbose_name='shipping')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='commerce.address', verbose_name='address')),
                ('items', models.ManyToManyField(related_name='order', to='commerce.Item', verbose_name='items')),
                ('promo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='commerce.promo', verbose_name='promo')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='commerce.orderstatus', verbose_name='status')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commerce.product', verbose_name='product'),
        ),
        migrations.AddField(
            model_name='item',
            name='properties',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='commerce.property', verbose_name='properties'),
        ),
        migrations.AddField(
            model_name='item',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.CreateModel(
            name='DeliveryMap',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('cost', models.DecimalField(decimal_places=0, max_digits=10, verbose_name='cost')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_map_destination', to='commerce.city', verbose_name='destination')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_map_source', to='commerce.city', verbose_name='source')),
            ],
            options={
                'verbose_name': 'delivery map',
                'verbose_name_plural': 'delivery map',
            },
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='commerce.city'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
