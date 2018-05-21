import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

from mobile_sale_app.forms import *
from mobile_sale_app.models import *
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q


# Create your views here.
# Trang chủ
def index(request):
    return render(request, 'mobile_sale_app/home.html')

# Lấy danh sách sản phẩm để show ra trang home
def get_product(request):
    # Loại sắp xếp: theo tên, theo giá
    field = request.GET.get('sort')
    order = request.GET.get('order')
    if order == 'asc':
        products_list = Product.objects.all().order_by(field)
    elif order == 'desc':
        field = '-' + field
        products_list = Product.objects.all().order_by(field)
    else:
        products_list = Product.objects.all().order_by('name')
    # Lấy ra 12 sản phẩm / trang để hiển thị
    paginator = Paginator(products_list, 12)
    page = 1
    try:
        # Lấy số trang
        page = request.GET.get('page')
        products = paginator.get_page(page)
    except PageNotAnInteger:
        # Nếu không thể lấy được (có lỗi) thì gán mặc định bằng 1
        products = paginator.get_page(1)
    except EmptyPage:
        products = paginator.get_page(1)
    return products

# Lấy danh sách sản phẩm
def listing_product(request):
    products = get_product(request)
    is_none = False
    return render(request, 'mobile_sale_app/home.html', {'products': products,
                                                         'is_none': is_none})

# Đăng ký
def signup(request):
    registered = False
    error = False
    # Lấy dữ liệu từ form để lưu vào database
    if request.method == "POST":
        customer_form = CustomerForm(data=request.POST)
        customer_profile_form = CustomerProfileInfoForm(data=request.POST)
        # Nếu form valid thì tiến hành lưu lại
        if customer_form.is_valid() and customer_profile_form.is_valid():
            customer = customer_form.save(commit=False)
            # Lấy username và password để authenticate sau đó
            username = customer_form.cleaned_data['username']
            password = customer_form.cleaned_data['password']
            customer.set_password(password)
            customer.save()

            customer_profile = customer_profile_form.save(commit=False)
            customer_profile.user = customer
            customer_profile.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    registered = True
                    # Tự động đăng nhập và redirect sang trang chủ
                    HttpResponseRedirect(reverse('mobile_sale_app:index'))
        else:
            print(customer_form.errors, customer_profile_form.errors)
            error = True
    # Có lỗi thì tạo 1 form mặc định để update UI
    else:
        error = False
        customer_form = CustomerForm()
        customer_profile_form = CustomerProfileInfoForm()
    return render(request, 'mobile_sale_app/signup.html',
                  {'customer_form': customer_form,
                   'customer_profile_form': customer_profile_form,
                   'registered': registered,
                   'error': error,
                   })

# Đăng xuất
# Cần phải đăng nhập mới dùng được chức năng này
@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('mobile_sale_app:index'))

# Đăng nhập
def log_in(request):
    error = False

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        # User tốn tại và đã active thì cho phép đăng nhập, chuyển qua trang chủ
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('mobile_sale_app:index'))
            # Báo lỗi
            else:
                error = True
                error_detail = "ACCOUNT IS NOT ACTIVE"
                return render(request, 'mobile_sale_app/login.html', {'error': error, 'error_detail': error_detail})

        else:
            print('Someone tried to login and failed')
            print("Username: {} and Password: {}".format(username, password))
            error = True
            error_detail = "Username or password is not correct"
            return render(request, 'mobile_sale_app/login.html', {'error': error, 'error_detail': error_detail})

    else:
        return render(request, 'mobile_sale_app/login.html', {})

# Log in vao trang quản lí
def admin_site_log_in(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active and user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('mobile_sale_app:manage_order'))

            else:
                return render(request, 'mobile_sale_app/admin_login.html')

        else:
            print('Someone tried to login and failed')
            print("Username: {} and Password: {}".format(username, password))
            error = True
            error_detail = "Username or password is not correct"
            return render(request, 'mobile_sale_app/admin_login.html')

    else:
        return render(request, 'mobile_sale_app/admin_login.html')


# Trang chi tiết của sản phẩm
def product_detail(request, pk):
    comment_form = CommentForm()
    try:
        product = Product.objects.get(id=pk)
        # Lấy ra các comment của sản phẩm
        comments = Comment.objects.filter(product__id=pk).order_by('time')
        size = comments.count()
        # Duyệt ra danh sách sản phẩm
        valid_profiles_id_list = Product.objects.all().values_list('id', flat=True)
        # Lấy ngẫu nhiên ra 3 sản phẩm để gợi ý
        random_profiles_id_list = random.sample(list(valid_profiles_id_list), min(len(valid_profiles_id_list), 3))
        other_products = Product.objects.filter(id__in=random_profiles_id_list)
    except Product.DoesNotExist:
        raise Http404('Product is not exist')
    return render(request, 'mobile_sale_app/product_detail.html', {'product': product,
                                                                   'other_products': other_products,
                                                                   'comments': comments,
                                                                   'size': size,
                                                                   'comment_form': comment_form})

# Thêm mới comment
def add_comment(request):
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        # rating = request.POST.get('rating')
        # print(rating)
        product_id = request.POST.get('product_id')
        rating = request.POST.get('rating')
        print(product_id)
        comment = comment_form.save(commit=False)
        # comment.rate = rating
        product = Product.objects.get(id=product_id)
        comment.product = product
        # Truy xuất ra user viết cái bình luận này
        account = get_customer_info(request)
        comment.customer = account
        comment.rate = rating
        comment.save()
        return HttpResponseRedirect(reverse('mobile_sale_app:product_detail', kwargs={'pk': product_id}))


# Mã hóa uid
def decode_string(value):
    result = ''
    for i in range(0, len(value), 5):
        result += value[i]
    result = result[:len(result) - 4]
    return result

<<<<<<< HEAD

# Thanh toán
=======
@login_required(login_url = '/login/')
>>>>>>> e8dfd314d2c57c6aed2dce8b5515fa12c601dc98
def payment(request, pd_id):
    product = Product.objects.get(id=pd_id)
    # Lấy dữ liệu từ form để thanh toán
    if request.method == 'POST':
        payment_form = PaymentForm(data=request.POST)
        if payment_form.is_valid():
            order = payment_form.save(commit=False)
            order.products = product
            try:
                account = request.user
                user = CustomerProfileInfo.objects.get(user=account)
                if user is not None:
                    order.user_id = user.id
                else:
                    order.user_id = ''
            except CustomerProfileInfo.DoesNotExist:
                order.user_id = ''
            order.save()
            return HttpResponseRedirect(reverse('mobile_sale_app:index'))
    else:
        try:
            account = request.user
            user = CustomerProfileInfo.objects.get(user=account)
            if user is not None:
                payment_form = PaymentForm(
                    data={
                        'customer_name': user.name,
                        'phone_no': user.phone_no,
                        'customer_address': user.address,
                        'email': account.email,
                        'deliver_to': user.address,
                        'note': '',
                    }
                )
            else:
                payment_form = PaymentForm()
        except User.DoesNotExist:
            payment_form = PaymentForm()
        except CustomerProfileInfo.DoesNotExist:
            payment_form = PaymentForm()
        return render(request, 'mobile_sale_app/payment.html', {'payment_form': payment_form,
                                                                'product': product,
                                                                })

<<<<<<< HEAD
# Hiển thị danh sách hàng của người dùng
=======

@login_required(login_url = '/login/')
>>>>>>> e8dfd314d2c57c6aed2dce8b5515fa12c601dc98
def customer_order(request):
    orders = None
    try:
        account = request.user
        user = CustomerProfileInfo.objects.get(user=account)
        if user is not None:
            # Show user's order
            orders = Order.objects.filter(user_id=user.id)
        else:
            return render(request, 'mobile_sale_app/login.html')
    except User.DoesNotExist:
        error = 'Something went wrong'
        return render(request, 'mobile_sale_app/login.html')
    except CustomerProfileInfo.DoesNotExist:
        return render(request, 'mobile_sale_app/customer_order.html', {'orders': orders})
    return render(request, 'mobile_sale_app/customer_order.html', {'orders': orders})


# Xóa đặt hàng
def delete_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order_delete = Order.objects.get(id=order_id)
        order_delete.delete()
        return HttpResponseRedirect(reverse('mobile_sale_app:customer_order'))
    else:
        return HttpResponseRedirect(reverse('mobile_sale_app:customer_order'))

# Trang admin hiển thị tất cả danh sách đơn hàng của hệ thống
# Cần quyền admin mới thực hiện được chức năng này
@user_passes_test(lambda u: u.is_superuser)
def admin_orders(request):
    orders = Order.objects.all()
    return render(request, 'mobile_sale_app/order_manage.html', {'orders': orders})

# Chỉnh sửa trạng thái order
@user_passes_test(lambda u: u.is_superuser)
def edit_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status_updated')
        print(order_id)
        print(new_status)
        order_update = Order.objects.get(id=order_id)
        if order_update is not None:
            order_update.status = int(new_status)
            order_update.save()
            print('OK')
        else:
            print('Error')
        return HttpResponseRedirect(reverse('mobile_sale_app:manage_order'))

# Lấy dữ liệu người dùng
def get_customer_info(request):
    user = request.user
    try:
        account = CustomerProfileInfo.objects.get(user=user)
    except CustomerProfileInfo.DoesNotExist:
        account = None
    return account

# Thay đổi info người dùng
@login_required
def change_user_info(request):
    if request.method == 'POST':
        account = get_customer_info(request)
        user_info_form = CustomerProfileInfoForm(data=request.POST, instance=account)
        account_email = request.POST.get('email')
        if user_info_form.is_valid():
            user_info = user_info_form.save(commit=False)
            user = request.user
            user.email = account_email
            user.save()
            user_info.save()
            return HttpResponseRedirect(reverse('mobile_sale_app:index'))
        else:
            account = get_customer_info(request)
            if account is not None:
                account_form = CustomerProfileInfoForm(initial={
                    'name': account.name,
                    'phone_no': account.phone_no,
                    'birth_day': account.birth_day,
                    'address': account.address,
                    'gender': account.gender,
                    'social_id': account.social_id
                })
                user_form = CustomerForm(initial={
                    'email': request.user.email
                })
            else:
                account_form = CustomerProfileInfoForm()
                user_form = CustomerForm()
    else:
        account = get_customer_info(request)
        if account is not None:
            account_form = CustomerProfileInfoForm(initial={
                'name': account.name,
                'phone_no': account.phone_no,
                'birth_day': account.birth_day,
                'address': account.address,
                'gender': account.gender,
                'social_id': account.social_id
            })
            user_form = CustomerForm(initial={
                'email': request.user.email
            })
        else:
            account_form = CustomerProfileInfoForm()
            user_form = CustomerForm()
    return render(request, 'mobile_sale_app/change_user_info.html', {'account_form': account_form,
                                                                     'user_form': user_form})

# Thay đổi mật khẩu
@login_required
def change_password(request):
    current_user = request.user
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password1')
        renew_password = request.POST.get('new_password2')
        user = authenticate(username=current_user.username, password=old_password)
        if user is not None and new_password == renew_password:
            user.set_password(new_password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('mobile_sale_app:index'))
        elif new_password != renew_password:
            error = 'Confirm new password is not match'
        form = ChangePasswordForm()
    else:
        form = ChangePasswordForm()
    return render(request, 'mobile_sale_app/change_password.html', {'change_password_form': form})

# Chức năng tìm kiếm
def search_product(request):
    keyword = request.GET.get('keyword')
    try:
        keyword = str(keyword)
        # Tìm kiếm theo tên sản phẩm, hệ điều hành, nhà sản xuất, mô tả sản phẩm, màu sắc
        results = Product.objects.filter(Q(name__contains=keyword) |
                                         Q(os__contains=keyword) |
                                         Q(manufacturer__contains=keyword) |
                                         Q(description__contains=keyword) |
                                         Q(color__contains=keyword))
        # Nếu ko có sản phẩm nào được tìm ra thì random vài sản phẩm gợi ý
        if results.count() < 1:
            is_none = True
            valid_profiles_id_list = Product.objects.all().values_list('id', flat=True)
            random_profiles_id_list = random.sample(list(valid_profiles_id_list), min(len(valid_profiles_id_list), 12))
            other_products = Product.objects.filter(id__in=random_profiles_id_list)
        else:
            is_none = False
            other_products = None
    except Exception as e:
        pass
    try:
        keyword = float(keyword)
        results = Product.objects.filter(Q(memory__exact=keyword) |
                                         Q(battery__exact=keyword) |
                                         Q(camera_resolution__exact=keyword) |
                                         Q(screen_size__exact=keyword))
        if results.count() < 1:
            is_none = True
            valid_profiles_id_list = Product.objects.all().values_list('id', flat=True)
            random_profiles_id_list = random.sample(list(valid_profiles_id_list), min(len(valid_profiles_id_list), 12))
            other_products = Product.objects.filter(id__in=random_profiles_id_list)
        else:
            is_none = False
            other_products = None
    except Exception as e:
        pass
    return render(request, 'mobile_sale_app/home.html', {'products': results,
                                                         'other_product': other_products,
                                                         'is_none': is_none,
                                                         'keyword': keyword})


# Các trang web tĩnh, chỉ hiển thị nội dung và ko có tương tác
# Trang giới thiệu
def intro(request):
    return render(request, 'mobile_sale_app/intro.html')

# Liên hệ
def contact_us(request):
    return render(request, 'mobile_sale_app/contact.html')

# Quy định bảo hành
def warranty_rule(request):
    return render(request, 'mobile_sale_app/warranty_rule.html')


# Quy định đổi trả
def exchange_regulations(request):
    return render(request, 'mobile_sale_app/exchange_regulations.html')

# Giao hàng
def delivery_regulations(request):
    return render(request, 'mobile_sale_app/delivery_regulations.html')

# cách thức thanh toán
def payment_regulations(request):
    return render(request, 'mobile_sale_app/payment_regulations.html')

# Thông tin về team
def about_team(request):
    return render(request, 'mobile_sale_app/about_team.html')
