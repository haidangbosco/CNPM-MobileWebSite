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
def index(request):
    return render(request, 'mobile_sale_app/home.html')


def get_product(request):
    field = request.GET.get('sort')
    order = request.GET.get('order')
    if order == 'asc':
        products_list = Product.objects.all().order_by(field)
    elif order == 'desc':
        field = '-' + field
        products_list = Product.objects.all().order_by(field)
    else:
        products_list = Product.objects.all().order_by('name')

    paginator = Paginator(products_list, 12)
    page = 1
    try:
        page = request.GET.get('page')
        products = paginator.get_page(page)
    except PageNotAnInteger:
        products = paginator.get_page(1)
    except EmptyPage:
        products = paginator.get_page(1)
    return products


def listing_product(request):
    products = get_product(request)
    is_none = False
    return render(request, 'mobile_sale_app/home.html', {'products': products,
                                                         'is_none': is_none})


def signup(request):
    registered = False
    error = False

    if request.method == "POST":
        customer_form = CustomerForm(data=request.POST)
        customer_profile_form = CustomerProfileInfoForm(data=request.POST)

        if customer_form.is_valid() and customer_profile_form.is_valid():
            customer = customer_form.save(commit=False)
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
                    HttpResponseRedirect(reverse('mobile_sale_app:index'))
        else:
            print(customer_form.errors, customer_profile_form.errors)
            error = True

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


@login_required
def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('mobile_sale_app:index'))


def log_in(request):
    error = False

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('mobile_sale_app:index'))

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


def product_detail(request, pk):
    comment_form = CommentForm()
    try:
        product = Product.objects.get(id=pk)
        comments = Comment.objects.filter(product__id=pk).order_by('time')
        size = comments.count()

        valid_profiles_id_list = Product.objects.all().values_list('id', flat=True)
        random_profiles_id_list = random.sample(list(valid_profiles_id_list), min(len(valid_profiles_id_list), 3))
        other_products = Product.objects.filter(id__in=random_profiles_id_list)
    except Product.DoesNotExist:
        raise Http404('Product is not exist')
    return render(request, 'mobile_sale_app/product_detail.html', {'product': product,
                                                                   'other_products': other_products,
                                                                   'comments': comments,
                                                                   'size': size,
                                                                   'comment_form': comment_form})


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
        account = get_customer_info(request)
        comment.customer = account
        comment.rate = rating
        comment.save()
        return HttpResponseRedirect(reverse('mobile_sale_app:product_detail', kwargs={'pk': product_id}))


def decode_string(value):
    result = ''
    for i in range(0, len(value), 5):
        result += value[i]
    result = result[:len(result) - 4]
    return result

@login_required(login_url = '/login/')
def payment(request, pd_id):
    product = Product.objects.get(id=pd_id)
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


@login_required(login_url = '/login/')
def customer_order(request):
    orders = None
    try:
        account = request.user
        user = CustomerProfileInfo.objects.get(user=account)
        if user is not None:
            # Show user's order
            orders = Order.objects.filter(user_id=user.id)
    except User.DoesNotExist:
        error = 'Something went wrong'
        return render(request, 'mobile_sale_app/customer_order.html', {'orders': orders})
    except CustomerProfileInfo.DoesNotExist:
        return render(request, 'mobile_sale_app/customer_order.html', {'orders': orders})
    return render(request, 'mobile_sale_app/customer_order.html', {'orders': orders})


def delete_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order_delete = Order.objects.get(id=order_id)
        order_delete.delete()
        return HttpResponseRedirect(reverse('mobile_sale_app:customer_order'))
    else:
        return HttpResponseRedirect(reverse('mobile_sale_app:customer_order'))


@user_passes_test(lambda u: u.is_superuser)
def admin_orders(request):
    orders = Order.objects.all()
    return render(request, 'mobile_sale_app/order_manage.html', {'orders': orders})


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


def get_customer_info(request):
    user = request.user
    try:
        account = CustomerProfileInfo.objects.get(user=user)
    except CustomerProfileInfo.DoesNotExist:
        account = None
    return account


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


def search_product(request):
    keyword = request.GET.get('keyword')
    try:
        keyword = str(keyword)
        results = Product.objects.filter(Q(name__contains=keyword) |
                                         Q(os__contains=keyword) |
                                         Q(manufacturer__contains=keyword) |
                                         Q(description__contains=keyword) |
                                         Q(color__contains=keyword))
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


def intro(request):
    return render(request, 'mobile_sale_app/intro.html')


def contact_us(request):
    return render(request, 'mobile_sale_app/contact.html')


def warranty_rule(request):
    return render(request, 'mobile_sale_app/warranty_rule.html')


def exchange_regulations(request):
    return render(request, 'mobile_sale_app/exchange_regulations.html')


def delivery_regulations(request):
    return render(request, 'mobile_sale_app/delivery_regulations.html')


def payment_regulations(request):
    return render(request, 'mobile_sale_app/payment_regulations.html')


def about_team(request):
    return render(request, 'mobile_sale_app/about_team.html')
