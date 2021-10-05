from typing import List

from ninja import Schema
from ninja.orm import create_schema
from pydantic import UUID4

from config.utils.schemas import Paginated
from account.schemas import AccountOut
from commerce.models import Property, Variant, Merchant, Label, Promo, Vendor, OrderStatus


class CitySchemaOut(Schema):
    pk: UUID4
    name: str
    # translations: Optional[List[CityTranslationSchemaOut]]


class AddressSchemaOut(Schema):
    pk: int
    work_address: bool
    address1: str
    address2: str
    long: float
    lat: float
    city: CitySchemaOut
    phone: str


class AddressCreateDataIn(Schema):
    work_address: bool
    address1: str
    address2: str
    long: float
    lat: float
    city: int
    phone: str


class CategoryDataOut(Schema):
    pk: int
    name: str
    description: str
    image: str
    slug: str
    children: List['CategoryDataOut'] = None


CategoryDataOut.update_forward_refs()

PropertyDataOut = create_schema(Property,
                                exclude=['created', 'updated', 'variant', 'barcode', 'merchant_barcode', 'cost'])

VariantDataOut = create_schema(Variant, exclude=['created', 'updated', 'product'])

PromoDataOut = create_schema(Promo, exclude=['created', 'updated', 'active_from', 'active_till'])

VendorDataOut = create_schema(Vendor, exclude=['created', 'updated'])


class VariantDetailDataOut(Schema):
    pk: int
    name: str
    value: str
    properties: List[PropertyDataOut]


MerchantDataOut = create_schema(Merchant, exclude=['created', 'updated', 'user'])


class ProductImageDataOut(Schema):
    pk: int
    image: str
    alt_text: str = None
    is_default_image: bool


LabelDataOut = create_schema(Label, exclude=['created', 'updated'])


class ProductDataOut(Schema):
    pk: UUID4
    name: str
    slug: str
    description: str
    in_stock: bool
    total_qty: int
    lowest: float
    lowest_discounted: float = None
    weight: float = None
    height: float = None
    length: float = None
    vendor: VendorDataOut
    category: CategoryDataOut
    merchant: MerchantDataOut
    is_featured: bool
    is_active: bool
    label: LabelDataOut
    variants: List[VariantDetailDataOut]
    images: List[ProductImageDataOut]


class PaginatedProductDataOut(Schema):
    total_count: int
    per_page: int
    from_record: int
    to_record: int
    previous_page: int
    current_page: int
    next_page: int
    page_count: int
    data: List[ProductDataOut]


class PaginatedProductManyOut(Paginated):
    data: List[ProductDataOut]


class ItemDataOut(Schema):
    pk: int
    product: ProductDataOut
    item_qty: int
    ordered: bool
    get_variants: VariantDataOut
    get_properties: PropertyDataOut


class ItemIn(Schema):
    slug: str
    properties: int
    item_qty: int = None


OrderStatusDataOut = create_schema(OrderStatus, exclude=['id', 'created', 'updated'])


class OrderDataOut(Schema):
    pk: int
    user: AccountOut
    address: AddressSchemaOut = None
    order_total: float
    status: OrderStatusDataOut
    note: str = None
    ref_code: str
    ordered: bool
    items: List[ItemDataOut]
    promo: PromoDataOut = None
    order_shipment: float = None


class OrderIn(Schema):
    items: List[int]


class NoteUpdateDataIn(Schema):
    note: str


class AddressUpdateDataIn(Schema):
    address_pk: int


class PromoDataIn(Schema):
    promo_code: str
    order_id: int
