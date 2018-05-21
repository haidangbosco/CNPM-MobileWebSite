import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

# Create your models here.

# Customer Model


class CustomerProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=True)
    # Additional
    name = models.CharField(max_length=264, blank=False)
    phone_no = models.CharField(max_length=11, blank=False)
    birth_day = models.DateField(default=datetime.date.today, blank=True)
    address = models.CharField(max_length=264, blank=False)
    social_id = models.CharField(max_length=10, blank=False)
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )
    gender = models.CharField(choices=GENDER, max_length=1, default=OTHER, blank=True)

    # Display of object
    def __str__(self):
        return self.name


# # Employee Model
# class Employee(models.Model):
#
#     # Attributes
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     last_name = models.CharField(max_length=264, blank=False)
#     first_name = models.CharField(max_length=264, blank=False)
#     birthday = models.DateField()
#     address = models.CharField(max_length=264, blank=False)
#     hometown = models.CharField(max_length=264, blank=True)
#     salary = models.FloatField(default=0)
#     phone_no = models.CharField(max_length=11, blank=False)
#     email = models.EmailField(blank=False)
#     # 1 - admin, 2 - courier, 3 - customer care
#     ADMIN = 'AD'
#     COURIER = 'CR'
#     CUSTOMER_CARE = 'CC'
#     KIND_OF_CUSTOMER = (
#         (ADMIN, 'Admin'),
#         (COURIER, 'Courier'),
#         (CUSTOMER_CARE, 'Customer Care')
#     )
#     type_employee = models.CharField(max_length=2, choices=KIND_OF_CUSTOMER, default=CUSTOMER_CARE)
#
#     # Display of object
#     def __str__(self):
#         return self.last_name + " " + self.first_name


def auto_increment_product_code():
    last_product = Product.objects.all().count()
    number = str(last_product).zfill(6)
    return 'SP' + number


# Product Model
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ANDROID = 'AND'
    IOS = 'IOS'
    WINDOW_PHONE = 'WDP'
    OTHER = 'OTH'
    OS_TYPE = (
        (ANDROID, 'Android'),
        (IOS, 'Ios'),
        (WINDOW_PHONE, 'Window phone'),
        (OTHER, 'Other'),
    )
    os = models.CharField(max_length=3, blank=True, choices=OS_TYPE, default=OTHER)
    name = models.CharField(max_length=264, blank=False)
    # SAMSUNG, APPLE, HTC, NOKIA, BLACK BERRY, OPPO, SONY, VIVO, HUAWEI, XIAOMI, ASUS, MOTOROLA,..
    SAMSUNG = 'SAM'
    APPLE = 'APP'
    HTC = 'HTC'
    NOKIA = 'NKA'
    BLACK_BERRY = 'BBR'
    OPPO = 'OPP'
    SONY = 'SN'
    VIVO = 'VV'
    HUAWEI = 'HW'
    XIAOMI = 'XM'
    ASUS = 'AS'
    MOTOROLA = 'MRL'
    OTHER = 'OTH'
    MANUFACTURER = (
        (SAMSUNG, 'Samsung'),
        (APPLE, 'Apple'),
        (HTC, 'HTC'),
        (NOKIA, 'Nokia'),
        (BLACK_BERRY, 'Black Berry'),
        (OPPO, 'Oppo'),
        (SONY, 'Sony'),
        (VIVO, 'Vivo'),
        (HUAWEI, 'Huawei'),
        (XIAOMI, 'Xiaomi'),
        (ASUS, 'Asus'),
        (MOTOROLA, 'Motorola'),
        (OTHER, 'Other'),
    )
    manufacturer = models.CharField(max_length=264, blank=True, choices=MANUFACTURER, default=OTHER)
    img = models.ImageField(upload_to='product_pics', blank=True)
    price = models.IntegerField(default=0)
    memory = models.FloatField(blank=False)
    camera_resolution = models.FloatField(blank=False)
    screen_size = models.FloatField(blank=False)
    weigth = models.FloatField(blank=False)
    color = models.CharField(max_length=10, blank=False)
    warranty = models.DateField(blank=False)
    sale = models.ForeignKey('Sale', on_delete=models.SET(''), blank=True)
    price_sale = models.IntegerField(default=0, editable=True)
    battery = models.IntegerField(blank=False)
    sound = models.CharField(blank=False, max_length=64)
    product_code = models.CharField(blank=False, default=auto_increment_product_code, max_length=8)
    description = models.CharField(max_length=500, blank=True)

    # Display of object
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "mobile_sale_app:product_detail",
            kwargs={
                # "slug": self.slug,
                "pk": self.pk
            }
        )

    def save(self, *args, **kwargs):
        self.price_sale = self.price - self.price * self.sale.sale_rate / 100
        super(Product, self).save(*args, **kwargs)


class Sale(models.Model):
    # Attributes
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=264)
    time_start = models.DateTimeField(blank=False)
    time_end = models.DateTimeField(blank=False)
    sale_rate = models.FloatField(blank=True, default=0)
    # Gift
    USB = 'USB'
    PEN = 'PEN'
    COUPON = 'COU'
    KEY_CHAINS = 'KEY'
    NONE = ''
    ITEM = (
        (NONE, 'None'),
        (USB, 'Usb'),
        (PEN, 'Pen'),
        (COUPON, 'Coupon'),
        (KEY_CHAINS, 'Keychains'),
    )
    item = models.CharField(max_length=3, choices=ITEM, default=NONE, blank=True)
    DISCOUNT = True
    BONUS_ITEM = False
    SALE_TYPE = (
        (DISCOUNT, 'Discount'),
        (BONUS_ITEM, 'Bonus Item'),
    )
    type = models.BooleanField(default=DISCOUNT, choices=SALE_TYPE)

    # Display of object
    def __str__(self):
        return self.name


# Order Model
class Order(models.Model):
    # 'customer_name', 'phone_no', 'email', 'customer_address', 'note', 'kind_delivery'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.TextField(blank=True, editable=True)
    products = models.ForeignKey('Product', on_delete=models.SET(''))  # OK
    customer_name = models.CharField(max_length=264, blank=False)  # OK
    phone_no = models.CharField(max_length=11, blank=False)  # OK
    email = models.EmailField(blank=True)  # OK
    customer_address = models.CharField(max_length=264, blank=False, default='')  # OK
    note = models.CharField(max_length=500, blank=True, default='')  # OK
    time_order = models.DateTimeField(default=datetime.datetime.now(), editable=False)
    deliver_to = models.CharField(max_length=264, blank=False)
    note = models.CharField(blank=True, max_length=264)  # OK
    DELIVERY_CHARGE = 20000
    EXPRESS = 'F'
    NORMAL = 'S'
    KIND_DELIVERY = (
        (EXPRESS, 'Chuyển phát nhanh'),
        (NORMAL, 'Chuyển hàng tiêu chuẩn')
    )
    kind_delivery = models.CharField(max_length=1, choices=KIND_DELIVERY, default=NORMAL)  # OK
    PAID = 1
    UNPAID = 0
    ON_WAY = 2
    STATUS = (
        (PAID, 'Đã thanh toán'),
        (UNPAID, 'Đang xử lí'),
        (ON_WAY, 'Đang vận chuyển'),
    )
    status = models.IntegerField(choices=STATUS, default=UNPAID)

    # Display of object
    def __str__(self):
        return self.products.name

    def get_total(self):
        if self.products.sale.type:
            if self.kind_delivery == 'F':
                return self.products.price_sale + self.DELIVERY_CHARGE
            else:
                return self.products.price_sale
        else:
            if self.kind_delivery == 'F':
                return self.products.price + self.DELIVERY_CHARGE
            else:
                return self.products.price


# Comment Model
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rate = models.IntegerField(default=5)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    customer = models.ForeignKey('CustomerProfileInfo', on_delete=models.CASCADE)
    time = models.DateTimeField(blank=False, default=datetime.datetime.now())
    content = models.CharField(blank=True, max_length=264)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
