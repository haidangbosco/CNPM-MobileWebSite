from django import forms
from django.contrib.auth.models import User
from mobile_sale_app.models import *
from django.contrib.auth.forms import *


class CustomerForm(forms.ModelForm):
    password = forms.PasswordInput(attrs={'class': 'form-control'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        labels = {
            'email': 'Email(*)',
            'username': 'Tên tài khoản(*)',
            'password': 'Mật khẩu(*)',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

        def __init__(self, *args, **kwargs):
            super(CustomerForm, self).__init__(*args, **kwargs)
            self.fields['username'].label = "Tên tài khoản"
            self.fields['password'].label = "Mật khẩu"


class CustomerProfileInfoForm(forms.ModelForm):
    class Meta:
        model = CustomerProfileInfo
        fields = ('name', 'phone_no', 'birth_day', 'address', 'gender', 'social_id')
        labels = {
            'name': "Họ và tên(*)",
            'phone_no': 'Số điện thoại(*)',
            'birth_day': "Ngày sinh",
            'address': 'Địa chỉ(*)',
            'gender': 'Giới tính',
            'social_id': 'Số CMND(*)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_day': forms.DateInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'social_id': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('customer_name', 'phone_no', 'email', 'customer_address', 'note', 'kind_delivery', 'deliver_to')
        labels = {
            'customer_name': 'Họ và tên',
            'phone_no': 'Số điện thoại',
            'email': 'Email',
            'customer_address': 'Địa chỉ',
            'note': 'Ghi chú',
            'kind_delivery': 'Cách giao hàng',
            'deliver_to': 'Nơi giao hàng'
        }
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ và tên'}),
            'phone_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'customer_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Địa chỉ'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ghi chú'}),
            'kind_delivery': forms.Select(attrs={'class': 'form-control'}),
            'deliver_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Địa chỉ nơi giao hàng'}),
        }


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Mật khẩu cũ', max_length=32, widget=forms.PasswordInput(
        attrs={'type': 'password', 'class': 'form-control'}))

    new_password1 = forms.CharField(label='Mật khẩu mới', max_length=32, widget=forms.PasswordInput(
        attrs={'type': 'password', 'class': 'form-control'}))

    new_password2 = forms.CharField(label='Xác nhận mật khẩu', max_length=32, widget=forms.PasswordInput(
        attrs={'type': 'password', 'class': 'form-control'}))

    def clean(self):
        if self.cleaned_data['new_password1'] != self.cleaned_data['new_password2']:
            raise forms.ValidationError("The two password fields did not match.")
        return self.cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Để lại bình luận'})
        }