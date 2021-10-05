import random
import string
from random import shuffle
from typing import List

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from ninja import Router

from config.utils import status
from config.utils.permissions import AuthBearer
from config.utils.schemas import MessageOut
from config.utils.utils import response
from commerce.models import City, Address, Vendor, Product, Category, Merchant, Label, PromoUsage, Order, Item, \
    OrderStatus, Promo, Property
from commerce.schemas import CitySchemaOut, AddressSchemaOut, AddressCreateDataIn, VendorDataOut, \
    PaginatedProductDataOut, CategoryDataOut, MerchantDataOut, LabelDataOut, OrderDataOut, OrderIn, NoteUpdateDataIn, \
    AddressUpdateDataIn, PromoDataIn, ItemDataOut, ItemIn

address = Router(tags=['address'])
vendor = Router(tags=['vendor'])
product = Router(tags=['product'])
order = Router(tags=['order'])
item = Router(tags=['order'])


@address.get('/city',
             response={200: List[CitySchemaOut], 404: MessageOut})
def city(request):
    cities = City.objects.all()
    if not cities.exists():
        return response(status.HTTP_404_NOT_FOUND, {'message': 'not found'})
    return response(status.HTTP_200_OK, cities)


@address.get('/address',
             auth=AuthBearer(),
             response={200: List[AddressSchemaOut], 404: MessageOut})
def list_address(request):
    address_qs = Address.objects.filter(user=request.auth).select_related('city')
    if not address_qs.exists():
        return response(status.HTTP_404_NOT_FOUND, {'message': 'not found'})
    return response(status.HTTP_200_OK, address_qs)


@address.get('/address/{pk}',
             response={200: AddressSchemaOut, 404: MessageOut})
def retrieve_address(request, pk: int):
    address_qs = Address.objects.filter(pk=pk, user=request.auth).select_related('city').first()
    if not address_qs:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'not found'})
    return response(status.HTTP_200_OK, address_qs)


@address.post('/address',
              response={400: MessageOut, 201: AddressSchemaOut})
def create_address(request, address_in: AddressCreateDataIn):
    address_data = address_in.dict()
    city_pk = address_data.pop('city')
    city_instance = get_object_or_404(City, pk=city_pk)
    address_qs = Address.objects.create(user=request.auth, **address_data, city=city_instance)
    if not address_qs:
        return response(status.HTTP_400_BAD_REQUEST, {'message': 'something went wrong'})
    return response(status.HTTP_201_CREATED, address_qs)


@address.put('/address/{pk}',
             response={200: AddressSchemaOut, 400: MessageOut})
def update_address(request, address_in: AddressCreateDataIn, pk: int):
    address_data = address_in.dict()
    city_pk = address_data.pop('city')
    city_instance = get_object_or_404(City, pk=city_pk)
    address_pk = Address.objects.filter(user=request.auth, pk=pk).update(**address_data, city=city_instance)
    address_qs = Address.objects.get(pk=address_pk)
    if not address_qs:
        return response(status.HTTP_400_BAD_REQUEST, {'message': 'something went wrong'})
    return response(status.HTTP_200_OK, address_qs)


@vendor.get('', auth=None, response={200: List[VendorDataOut]})
def all_vendors(request):
    return Vendor.objects.all()


@product.get('/all', auth=None, response={200: PaginatedProductDataOut})
def all_products(request, lowest_gte=None, lowest_lte=None, category_name=None,
                 merchant_name=None, vendor_name=None, is_featured=None, label_name=None,
                 search=None, per_page: int = 10, page: int = 1,
                 ):
    products_qs = Product.objects.filter(is_active=True).select_related('category', 'vendor', 'merchant')
    if lowest_gte:
        products_qs = products_qs.filter(lowest__gte=lowest_gte)
    if lowest_lte:
        products_qs = products_qs.filter(lowest__lte=lowest_lte)
    if category_name:
        products_qs = products_qs.filter(category__name=category_name)
    if merchant_name:
        products_qs = products_qs.filter(merchant__name=merchant_name)
    if vendor_name:
        products_qs = products_qs.filter(vendor__name=vendor_name)
    if is_featured:
        products_qs = products_qs.filter(is_featured=is_featured)
    if label_name:
        products_qs = products_qs.filter(label__name=label_name)

    if search:
        products_qs = products_qs.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    return response(status.HTTP_200_OK, products_qs, paginated=True, per_page=per_page, page=page)


@product.get('/{pk}/related', auth=None, response={200: PaginatedProductDataOut, 404: MessageOut})
def related_products(request, pk: int, per_page: int = 10, page: int = 1):
    try:
        product_qs = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'Product not found'})

    related = product_qs.tags.similar_objects()

    # print("-------", len(related))

    if not related:
        return response(status.HTTP_404_NOT_FOUND, {"message": "No related products found"})

    return response(status.HTTP_200_OK, related, paginated=True, per_page=per_page, page=page)


@product.get('/categories', auth=None, response=List[CategoryDataOut])
def categories(request):
    return Category.objects.order_by('pk').filter(is_active=True).filter(parent=None)


@product.get('/category/{cat_id}/products', auth=None, response={404: MessageOut, 200: PaginatedProductDataOut})
def cat_products(request, cat_id: int, per_page: int = 10, page: int = 1):
    if cat_id is None:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'No category specified'})
    try:
        category = Category.objects.get(pk=cat_id)
    except Category.DoesNotExist:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'Category does not exist'})
    products = (
        Product
            .objects
            .filter(category__in=category.get_descendants(include_self=True))
            .select_related('category', 'vendor', 'merchant')
    )

    shuffle(products)

    return response(status.HTTP_200_OK, products, paginated=True, per_page=per_page, page=page)


@product.get('/merchants', auth=None, response=List[MerchantDataOut])
def all_merchants(request):
    return Merchant.objects.all().order_by('pk')


@product.get('/labels', auth=None, response=List[LabelDataOut])
def all_labels(request):
    return Label.objects.all().order_by('pk')


def time_active_promo(promo):
    seconds_from = (timezone.now() - promo.active_from).total_seconds()
    # print(seconds_from)
    seconds_to = (timezone.now() - promo.active_till).total_seconds()
    # print(seconds_to)
    return seconds_from > 1 and seconds_to < 1


def usage_active_promo(user, promo):
    usage = PromoUsage.objects.filter(user=user).filter(promo=promo)
    return not usage.exists()


def create_ref_code() -> str:
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


@order.get('/all', response={200: List[OrderDataOut], 404: MessageOut})
def all_orders(request, ordered: bool = False):
    order_qs = Order.objects.order_by('pk').filter(user=request.auth.get('user'))
    if not ordered:
        order_qs = order_qs.filter(ordered=ordered)
    if not order_qs:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'no active orders'})
    return response(status.HTTP_200_OK, order_qs)


@order.post('/create_update', response={200: MessageOut, 401: MessageOut})
def create_update(request, items_in: OrderIn):
    user = request.auth.get('user', None)
    if not user:
        return response(status.HTTP_401_UNAUTHORIZED, {'message': 'unauthorized'})
    items = Item.objects.filter(id__in=items_in.items)

    existing_order = Order.objects.filter(user=user, ordered=False)

    if existing_order.exists():
        order_ = existing_order.first()
        for i in items:
            i.ordered = True
            i.save()
        order_.items.add(*items)
        order_.save()
        return response(status.HTTP_200_OK, {"message": "order updated successfully"})
    else:
        for i in items:
            i.ordered = True
            i.save()
        default_status = OrderStatus.objects.get(title="NEW")
        order_ = Order.objects.create(
            user=user,
            status=default_status,
            ordered=False,
            ref_code=create_ref_code(),
        )
        order_.items.add(*items)
        order_.save()
        return response(status.HTTP_200_OK, {"message": "order created successfully"})


@order.post('/checkout', response={200: MessageOut, 404: MessageOut, 400: MessageOut})
def checkout(request):
    try:
        checkout_order = Order.objects.get(ordered=False, user=request.auth.get('user'))
    except Order.DoesNotExist:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'Order not found'})

    if not checkout_order.address:
        return response(status.HTTP_400_BAD_REQUEST, {'message': 'order should have an address assigned'})

    checkout_order.shipping = checkout_order.order_shipment
    checkout_order.total = checkout_order.order_total
    for i in checkout_order.items.all():
        if i.properties.qty < i.item_qty:
            return response(status.HTTP_404_NOT_FOUND, {
                'message': f'item {i.product.name} - {i.properties.variant.name} - {i.properties.name} is out of stock!'
            })
        i.properties.qty -= i.item_qty
        i.properties.save()
    checkout_order.ordered = True
    checkout_order.save()
    return response(status.HTTP_200_OK, {'message': 'checkout successful'})


@order.post('/{pk}/update_note', response={200: MessageOut, 404: MessageOut})
def update_note(request, pk: int, data_in: NoteUpdateDataIn):
    try:
        order_qs = Order.objects.get(pk=pk, user=request.auth.get('user'))
    except Order.DoesNotExist:
        return response(status.HTTP_200_OK, {'message': 'Order does not exist'})

    order_qs.note = data_in.note
    order_qs.save()

    return response(status.HTTP_200_OK, {'message': 'order updated successfully'})


@order.post('/{pk}/update_address', response={200: MessageOut, 404: MessageOut})
def update_address(request, pk: int, data_in: AddressUpdateDataIn):
    try:
        address = Address.objects.get(pk=data_in.address_pk, user=request.auth.get('user'))
    except Address.DoesNotExist:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'Address does not exist'})

    try:
        order_qs = Order.objects.get(pk=pk, user=request.auth.get('user'))
    except Order.DoesNotExist:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'Order does not exist'})

    order_qs.address = address
    order_qs.save()

    return response(status.HTTP_200_OK, {'message': 'address updated successfully'})


@order.post('/promo', response={200: MessageOut, 400: MessageOut})
def add_promo(request, data_in: PromoDataIn):
    try:
        promo = Promo.objects.get(code=data_in.promo_code)
    except Promo.DoesNotExist:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'Address does not exist'})

    try:
        order_qs = Order.objects.get(pk=data_in.order_id, user=request.auth.get('user'))
    except Order.DoesNotExist:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'Order does not exist'})

    if not promo.is_active:
        return 400, {'message': 'promo code is not valid'}
    elif time_active_promo(promo) and usage_active_promo(request.auth.get('user'), promo):
        if promo.user:
            if str(promo.user.phone_number) != str(request.auth.get('user')):
                return response(status.HTTP_400_BAD_REQUEST,
                                {'message': 'Promo code is not valid or not allowed for you'})

            order_qs.promo = promo
            order_qs.save()
            PromoUsage.objects.create(promo=promo, user=request.auth.get('user'))
            return response(status.HTTP_200_OK, {'message': 'Promo applied successfully'})
        else:
            order_qs.promo = promo
            order_qs.save()
            PromoUsage.objects.create(promo=promo, user=request.auth.get('user'))
            return response(status.HTTP_200_OK, {'message': 'promo code added successfully'})
    else:
        return response(status.HTTP_200_OK, {'message': 'promo code is not valid or used'})


@item.get('/all', response={404: MessageOut, 200: List[ItemDataOut]})
def all_items(request):
    item_qs = Item.objects.order_by('pk').filter(user=request.auth.get('user')).filter(ordered=False)
    if not item_qs:
        return response(status.HTTP_404_NOT_FOUND, {"message": "Your cart is empty"})

    else:
        return response(status.HTTP_200_OK, item_qs)


@item.get('/get/{item_pk}', response={200: ItemDataOut, 404: MessageOut})
def get_item(request, item_pk: int):
    _item = Item.objects.filter(pk=item_pk).filter(user=request.auth.get('user'))

    if not _item:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'Item does not exist'})

    return response(status.HTTP_200_OK, _item.first())


@item.post('/add_to_cart', response={200: MessageOut, 400: MessageOut, 403: MessageOut, 401: MessageOut})
def add_to_cart(request, item_in: ItemIn):
    user = request.auth.get('user')
    if not user:
        return response(status.HTTP_401_UNAUTHORIZED, {'message': 'unauthorized'})
    slug = item_in.slug
    properties = item_in.properties
    item_qty = item_in.item_qty or 1

    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        return response(status.HTTP_404_NOT_FOUND, {"message": "Product does not exist"})

    item_qs = Item.objects.filter(
        product=product,
        user=request.auth.get('user'),
        ordered=False
    )

    # properties_integrity represents whether properties products belong to or not
    # if the product doesn't belong to request properties, then there is a
    # properties integrity error
    properties_integrity = (Product.objects
                            .filter(slug__exact=product.slug)
                            .filter(variants__properties=properties)
                            .count()
                            )
    item_qs = item_qs.filter(
        properties__exact=properties
    )

    try:
        properties_qs = Property.objects.get(pk=properties)
    except Property.DoesNotExist:
        return response(status.HTTP_400_BAD_REQUEST, {'message': 'property does not exist'})

    if properties_qs.qty < item_qty:
        return response(status.HTTP_403_FORBIDDEN, {'message': 'not enough in stock!'})

    if item_qs.exists():
        _item = item_qs.first()
        _item.item_qty += item_qty
        _item.save()
        #     properties_qs.qty -= item_qty
        #     properties_qs.save()
        return response(status.HTTP_200_OK, {"message": "already in cart, increased the quantity"})

    elif properties_integrity:
        _item = Item.objects.create(
            product=product,
            user=request.auth.get('user'),
            item_qty=item_qty,
            properties=properties_qs,
            ordered=False
        )

        _item.save()
        return response(status.HTTP_200_OK, {"message": "item added to cart successfully"})

    else:
        return response(status.HTTP_400_BAD_REQUEST, {'error': 'properties integrity error'})


@item.post('/increase_item_qty/{item_pk}', response={200: MessageOut, 404: MessageOut})
def increase_item_qty(request, item_pk: int):
    try:
        _item = Item.objects.get(pk=item_pk)
    except Item.DoesNotExist:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'Item does not exist'})

    _item.item_qty += 1
    _item.save()

    return response(status.HTTP_200_OK, {'message': 'item quantity increased successfully'})


@item.post('/decrease_item_qty/{item_pk}', response={200: MessageOut, 204: MessageOut, 404: MessageOut})
def decrease_item_qty(request, item_pk: int):
    try:
        _item = Item.objects.get(pk=item_pk)
    except Item.DoesNotExist:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'Item does not exist'})

    if _item.item_qty > 1:
        _item.item_qty -= 1
        _item.save()
    else:
        _item.delete()
        return response(status.HTTP_204_NO_CONTENT, {'message': 'item deleted'})
    return response(status.HTTP_200_OK, {'message': 'item quantity decreased successfully'})


@item.delete('/delete/{item_pk}', response={204: MessageOut, 404: MessageOut})
def delete_item(request, item_pk: int):
    _item = Item.objects.filter(pk=item_pk).filter(user=request.auth.get('user'))

    if not _item:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'Item does not exist'})

    _item.first().delete()

    return response(status.HTTP_204_NO_CONTENT, {'message': 'Item deleted'})
