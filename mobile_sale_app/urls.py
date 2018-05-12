from django.conf.urls import url
from mobile_sale_app import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from mobile_sale_app import views

app_name = 'mobile_sale_app'

urlpatterns = [
    url(r'^home/$', views.listing_product, name='index'),
    url(r'^signup/$', views.signup, name='sign_up'),
    url(r'^login/$', views.log_in, name='log_in'),
    url(r'^logout/$', views.log_out, name='log_out'),
    url(r'^(?P<pk>[0-9a-f-]+)/$', views.product_detail, name='product_detail'),
    url(r'^payment/(?P<pd_id>[0-9a-f-]+)/$', views.payment, name='payment'),
    url(r'^order/$', views.customer_order, name='customer_order'),
    url(r'^order/delete-order/$', views.delete_order, name='delete_order'),
    url(r'^admin-site/$', views.admin_site_log_in, name='admin_login'),
    url(r'^manage-order/$', views.admin_orders, name='manage_order'),
    url(r'^edit-order/$', views.edit_order, name='edit_order'),
    url(r'^change-info/$', views.change_user_info, name='change_user_info'),
    url(r'^change-password/$', views.change_password, name='change_password'),
    url(r'^search/$', views.search_product, name='search_product'),
    url(r'^intro/$', views.intro, name='intro'),
    url(r'^contact/$', views.contact_us, name='contact_us'),
    url(r'^warranty-rule/$', views.warranty_rule, name='warranty_rule'),
    url(r'^exchange-regulations/$', views.exchange_regulations, name='exchange_regulations'),
    url(r'^delivery-regulations/$', views.delivery_regulations, name='delivery_regulations'),
    url(r'^payment-regulations/$', views.payment_regulations, name='payment_regulations'),
    url(r'^about-team/$', views.about_team, name='about_team'),
    url(r'^$', views.listing_product, name='index'),
    url(r'^add-comment/$', views.add_comment, name='add_comment'),
]